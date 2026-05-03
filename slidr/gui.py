"""Main GUI for Slidr - AI Presentation Maker v2.2"""

import sys
import os
from datetime import datetime
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTextEdit, QCheckBox,
    QRadioButton, QButtonGroup, QFileDialog, QMessageBox,
    QProgressBar, QGroupBox, QComboBox, QFrame, QTabWidget,
    QListWidget, QListWidgetItem, QStackedWidget, QScrollArea
)
from PySide6.QtCore import Qt, QThread, Signal, QSize
from PySide6.QtGui import QFont
from slidr.config import TEMPLATES
from slidr.processors import FileProcessor
from slidr.generator import AIClient
from slidr.exporters import PPTXExporter, PDFExporter, HTMLExporter
from slidr.image_search import ImageSearch

SLIDE_TYPES = {
    "title": "Title Slide - Big title with subtitle",
    "content": "Content - Title and bullet points",
    "bullets_image": "Bullets + Image - Left bullets, right image",
    "two_column": "Two Column - Two content columns",
    "divider": "Divider - Section transition"
}


class GenerationThread(QThread):
    progress = Signal(str)
    finished = Signal(list)
    error = Signal(str)

    def __init__(self, client, topic=None, file_path=None, num_slides=6):
        super().__init__()
        self.client = client
        self.topic = topic
        self.file_path = file_path
        self.num_slides = num_slides

    def run(self):
        try:
            self.progress.emit("Generating slides...")
            if self.file_path:
                text = FileProcessor.extract_text(self.file_path)
                slides = self.client.generate_from_text(text, self.num_slides)
            else:
                slides = self.client.generate_slides(self.topic, self.num_slides)
            self.progress.emit("Done")
            self.finished.emit(slides)
        except Exception as e:
            self.error.emit(str(e))


class SlideEditorWidget(QWidget):
    """Widget for editing a single slide"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.slide_data = {}
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        
        # Type selector
        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel("Layout:"))
        self.type_combo = QComboBox()
        for t, desc in SLIDE_TYPES.items():
            self.type_combo.addItem(desc, t)
        type_layout.addWidget(self.type_combo)
        type_layout.addStretch()
        layout.addLayout(type_layout)
        
        # Title
        layout.addWidget(QLabel("Title:"))
        self.title_edit = QLineEdit()
        self.title_edit.setPlaceholderText("Slide title...")
        layout.addWidget(self.title_edit)
        
        # Subtitle
        layout.addWidget(QLabel("Subtitle:"))
        self.subtitle_edit = QLineEdit()
        self.subtitle_edit.setPlaceholderText("Optional subtitle...")
        layout.addWidget(self.subtitle_edit)
        
        # Bullets
        layout.addWidget(QLabel("Bullet Points:"))
        self.bullets_edit = QTextEdit()
        self.bullets_edit.setPlaceholderText("Enter one bullet point per line...")
        self.bullets_edit.setMaximumHeight(120)
        layout.addWidget(self.bullets_edit)
        
        # Image keywords
        layout.addWidget(QLabel("Image:"))
        
        image_layout = QHBoxLayout()
        self.image_keywords_edit = QLineEdit()
        self.image_keywords_edit.setPlaceholderText("Image URL (paste direct link)...")
        image_layout.addWidget(self.image_keywords_edit)
        
        self.search_image_btn = QPushButton("Add")
        self.search_image_btn.setStyleSheet("padding: 5px 10px;")
        image_layout.addWidget(self.search_image_btn)
        layout.addLayout(image_layout)
        
        # Helper text
        help_label = QLabel("Tip: Right-click image → Copy image address")
        help_label.setStyleSheet("color: #888; font-size: 10px;")
        layout.addWidget(help_label)
        
        # Image results
        self.image_status = QLabel("No image URL - paste a direct image link")
        self.image_status.setStyleSheet("color: #666; font-size: 11px; padding: 5px;")
        layout.addWidget(self.image_status)
        
        layout.addStretch()
    
    def load_slide(self, slide_data: dict):
        self.slide_data = slide_data
        slide_type = slide_data.get("type", "content")
        
        # Set combo box
        for i in range(self.type_combo.count()):
            if self.type_combo.itemData(i) == slide_type:
                self.type_combo.setCurrentIndex(i)
                break
        
        self.title_edit.setText(slide_data.get("title", ""))
        self.subtitle_edit.setText(slide_data.get("subtitle", ""))
        
        bullets = slide_data.get("bullets", [])
        self.bullets_edit.setText("\n".join(bullets))
        
        self.image_keywords_edit.setText(slide_data.get("image_keywords", ""))
    
    def get_slide_data(self) -> dict:
        bullets_text = self.bullets_edit.toPlainText()
        bullets = [b.strip() for b in bullets_text.split("\n") if b.strip()]
        
        return {
            "type": self.type_combo.currentData(),
            "title": self.title_edit.text(),
            "subtitle": self.subtitle_edit.text(),
            "bullets": bullets,
            "image_keywords": self.image_keywords_edit.text(),
            "notes": self.slide_data.get("notes", "")
        }


class SlidrWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ai_client = AIClient()
        self.image_search = ImageSearch()
        self.generation_thread = None
        self.current_slides = []
        self.input_file = None
        self.edited_slides = []
        self.selected_image_url = None

        self.setWindowTitle("Slidr - AI Presentation Maker v2.4")
        self.setGeometry(100, 100, 900, 700)

        self._setup_ui()

    def _setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        
        # Title
        title_label = QLabel("Slidr")
        title_label.setStyleSheet("font-size: 28px; font-weight: bold; color: #4A90D9;")
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Tab widget
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        
        # Tab 1: Generate
        self.generate_tab = self._create_generate_tab()
        self.tabs.addTab(self.generate_tab, "Generate")
        
        # Tab 2: Edit Slides
        self.edit_tab = self._create_edit_tab()
        self.tabs.addTab(self.edit_tab, "Edit Slides")
        
        # Tab 3: Export
        self.export_tab = self._create_export_tab()
        self.tabs.addTab(self.export_tab, "Export")
        
        main_layout.addWidget(self.tabs)
        
        # Initialize theme (default dark)
        self.dark_mode = True
        self._apply_theme()
        
        # Theme toggle button
        theme_btn = QPushButton("🌙" if self.dark_mode else "☀️")
        theme_btn.setFixedSize(40, 40)
        theme_btn.setStyleSheet("font-size: 18px; border: none; background: transparent;")
        theme_btn.clicked.connect(self._toggle_theme)
        main_layout.addWidget(theme_btn, 0, Qt.AlignRight)

    def _create_generate_tab(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(15)
        
        # Input group
        input_group = QGroupBox("Input")
        input_layout = QVBoxLayout(input_group)
        
        self.topic_input = QLineEdit()
        self.topic_input.setPlaceholderText("Enter your presentation topic...")
        self.topic_input.setStyleSheet("padding: 10px; font-size: 14px;")
        input_layout.addWidget(self.topic_input)
        
        or_label = QLabel("  OR  ")
        or_label.setStyleSheet("color: #999;")
        input_layout.addWidget(or_label)
        
        file_layout = QHBoxLayout()
        self.file_input = QLineEdit()
        self.file_input.setPlaceholderText("Select PDF or DOCX file...")
        self.file_input.setReadOnly(True)
        file_layout.addWidget(self.file_input)
        
        browse_btn = QPushButton("Browse")
        browse_btn.clicked.connect(self._browse_file)
        file_layout.addWidget(browse_btn)
        input_layout.addLayout(file_layout)
        
        # Slide count
        count_layout = QHBoxLayout()
        count_layout.addWidget(QLabel("Number of slides:"))
        self.slide_count_combo = QComboBox()
        for i in range(4, 13):
            self.slide_count_combo.addItem(str(i), i)
        self.slide_count_combo.setCurrentIndex(2)  # Default 6
        count_layout.addWidget(self.slide_count_combo)
        count_layout.addStretch()
        input_layout.addLayout(count_layout)
        
        layout.addWidget(input_group)
        
        # Generate button
        generate_btn = QPushButton("Generate Presentation")
        generate_btn.setStyleSheet("""
            QPushButton { background-color: #4A90D9; color: white; padding: 12px;
                font-size: 16px; font-weight: bold; border: none; border-radius: 5px; }
            QPushButton:hover { background-color: #357ABD; }
        """)
        generate_btn.clicked.connect(self._generate)
        layout.addWidget(generate_btn)
        
        # Progress
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("color: #666; font-size: 12px;")
        layout.addWidget(self.status_label)
        
        layout.addStretch()
        return widget

    def _create_edit_tab(self) -> QWidget:
        widget = QWidget()
        layout = QHBoxLayout(widget)
        
        # Left: Slide list
        left_panel = QFrame()
        left_panel.setFrameStyle(QFrame.StyledPanel)
        left_layout = QVBoxLayout(left_panel)
        
        left_layout.addWidget(QLabel("Slides:"))
        
        self.slide_list = QListWidget()
        self.slide_list.itemClicked.connect(self._on_slide_selected)
        left_layout.addWidget(self.slide_list)
        
        layout.addWidget(left_panel, 1)
        
        # Right: Slide editor
        right_panel = QFrame()
        right_panel.setFrameStyle(QFrame.StyledPanel)
        right_layout = QVBoxLayout(right_panel)
        
        right_layout.addWidget(QLabel("Edit Slide:"))
        
        self.slide_editor = SlideEditorWidget()
        # Connect search button
        main_window = self.parent() or self
        if hasattr(main_window, '_search_image'):
            self.slide_editor.search_image_btn.clicked.connect(main_window._search_image)
        right_layout.addWidget(self.slide_editor)
        
        # Save button
        save_btn = QPushButton("Save Changes")
        save_btn.clicked.connect(self._save_slide)
        right_layout.addWidget(save_btn)
        
        layout.addWidget(right_panel, 2)
        
        # Configure
        layout.setStretchFactor(left_panel, 1)
        layout.setStretchFactor(right_panel, 2)
        
        return widget

    def _create_export_tab(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(15)
        
        # Template selection
        template_group = QGroupBox("Template")
        template_layout = QVBoxLayout(template_group)
        
        self.template_group = QButtonGroup()
        self.template_radios = {}
        
        for key, config in TEMPLATES.items():
            radio = QRadioButton(config["name"])
            radio.setToolTip(config["description"])
            self.template_group.addButton(radio)
            self.template_radios[radio] = key
            template_layout.addWidget(radio)
        
        # Set default
        first_radio = list(self.template_radios.keys())[0]
        first_radio.setChecked(True)
        
        layout.addWidget(template_group)
        
        # Output formats
        format_group = QGroupBox("Output Formats")
        format_layout = QVBoxLayout(format_group)
        
        self.check_pptx = QCheckBox("PPTX (PowerPoint)")
        self.check_pptx.setChecked(True)
        format_layout.addWidget(self.check_pptx)
        
        self.check_pdf = QCheckBox("PDF")
        format_layout.addWidget(self.check_pdf)
        
        self.check_html = QCheckBox("HTML (Web)")
        format_layout.addWidget(self.check_html)
        
        layout.addWidget(format_group)
        
        # Export button
        export_btn = QPushButton("Export Presentation")
        export_btn.setStyleSheet("""
            QPushButton { background-color: #27AE60; color: white; padding: 12px;
                font-size: 16px; font-weight: bold; border: none; border-radius: 5px; }
            QPushButton:hover { background-color: #219A52; }
        """)
        export_btn.clicked.connect(self._export)
        layout.addWidget(export_btn)
        
        layout.addStretch()
        return widget

    def _browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Input File", "",
            "Documents (*.pdf *.docx *.doc);;PDF Files (*.pdf);;Word Documents (*.docx *.doc)"
        )
        if file_path:
            self.input_file = file_path
            self.file_input.setText(os.path.basename(file_path))
            self.topic_input.clear()

    def _generate(self):
        topic = self.topic_input.text().strip()
        file_path = self.input_file

        if not topic and not file_path:
            QMessageBox.warning(self, "Input Required", "Please enter a topic or select a file.")
            return

        self.status_label.setText("Connecting to Ollama...")
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)

        num_slides = self.slide_count_combo.currentData()
        
        self.generation_thread = GenerationThread(
            self.ai_client,
            topic=topic if topic else None,
            file_path=file_path,
            num_slides=num_slides
        )
        self.generation_thread.progress.connect(self._on_progress)
        self.generation_thread.finished.connect(self._on_generated)
        self.generation_thread.error.connect(self._on_error)
        self.generation_thread.start()

    def _on_progress(self, message):
        self.status_label.setText(message)

    def _on_generated(self, slides):
        self.progress_bar.setVisible(False)
        self.current_slides = slides
        self.edited_slides = slides.copy()
        
        # Update slide list
        self.slide_list.clear()
        for i, slide in enumerate(slides):
            slide_type = slide.get("type", "content")
            title = slide.get("title", f"Slide {i+1}")
            self.slide_list.addItem(f"[{slide_type}] {title}")
        
        # Count by type
        type_counts = {}
        for s in slides:
            t = s.get("type", "content")
            type_counts[t] = type_counts.get(t, 0) + 1
        
        type_summary = ", ".join([f"{v} {k}" for k, v in type_counts.items()])
        self.status_label.setText(f"Generated {len(slides)} slides: {type_summary}")
        
        # Switch to edit tab
        self.tabs.setCurrentIndex(1)
        
        # Select first slide
        if slides:
            self.slide_list.setCurrentRow(0)
            self._on_slide_selected(self.slide_list.currentItem())

    def _on_error(self, error):
        self.progress_bar.setVisible(False)
        self.status_label.setText("Error")
        QMessageBox.critical(self, "Generation Error", f"Failed to generate: {error}")

    def _on_error(self, error):
        self.progress_bar.setVisible(False)
        self.status_label.setText("Error")
        QMessageBox.critical(self, "Generation Error", f"Failed to generate: {error}")

    def _on_slide_selected(self, item):
        row = self.slide_list.row(item)
        if row < len(self.edited_slides):
            slide = self.edited_slides[row]
            self.slide_editor.load_slide(slide)
            # Load saved image
            saved_url = slide.get("image_url")
            if saved_url:
                self.selected_image_url = saved_url
                self.slide_editor.image_status.setText("Image loaded from slide")
            else:
                self.selected_image_url = None
                self.slide_editor.image_status.setText("No image selected")

    def _search_image(self):
        """Search for image based on keywords"""
        keywords = self.slide_editor.image_keywords_edit.text().strip()
        if not keywords:
            QMessageBox.warning(self, "No Keywords", "Enter keywords to search for images.")
            return
        
        self.slide_editor.image_status.setText("Searching...")
        QApplication.processEvents()
        
        results = self.image_search.search_unsplash(keywords, 6)
        
        if not results:
            results = self.image_search._get_demo_images(keywords, 3)
        
        # Show results
        if results and results[0].get("url"):
            # Show first result
            self.selected_image_url = results[0].get("url")
            desc = results[0].get("description", keywords)
            self.slide_editor.image_status.setText(f"✓ Selected: {desc[:40]}...")
        else:
            self.selected_image_url = None
            # Show placeholder info
            self.slide_editor.image_status.setText(f"Demo: {keywords} - Use image from online/paste URL")

    def _save_slide(self):
        current_row = self.slide_list.currentRow()
        if current_row < len(self.edited_slides):
            slide_data = self.slide_editor.get_slide_data()
            
            # Save image URL - read directly from the input field
            image_url = self.slide_editor.image_keywords_edit.text().strip()
            
            # Check if it looks like a URL
            if image_url and ("http" in image_url or "." in image_url):
                # It's a URL - save it
                slide_data["image_url"] = image_url
                self.slide_editor.image_status.setText("✅ Image URL saved!")
            
            self.edited_slides[current_row] = slide_data
            
            # Update list item
            slide = self.edited_slides[current_row]
            slide_type = slide.get("type", "content")
            title = slide.get("title", f"Slide {current_row+1}")
            
            # Show image indicator
            img_indicator = " 📷" if slide.get("image_url") else ""
            self.slide_list.currentItem().setText(f"[{slide_type}] {title}{img_indicator}")
            
            msg = "Slide changes saved!"
            if slide.get("image_url"):
                msg += " Image added!"
            QMessageBox.information(self, "Saved", msg)

    def _export(self):
        if not self.edited_slides:
            QMessageBox.warning(self, "No Slides", "Please generate slides first.")
            return

        slides = self.edited_slides
        
        # Get template
        template = "minimal"
        for radio, key in self.template_radios.items():
            if radio.isChecked():
                template = key
                break
        
        # Output path
        base_name = f"presentation_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        output_dir = os.path.join(os.path.expanduser("~"), "Documents")
        
        exported = []
        
        try:
            if self.check_pptx.isChecked():
                output_path = os.path.join(output_dir, f"{base_name}.pptx")
                PPTXExporter.export(slides, "Presentation", output_path, template)
                exported.append(output_path)

            if self.check_pdf.isChecked():
                output_path = os.path.join(output_dir, f"{base_name}.pdf")
                try:
                    PDFExporter.export(slides, "Presentation", output_path, template)
                    exported.append(output_path)
                except ImportError as e:
                    QMessageBox.warning(self, "PDF Warning", f"Could not export PDF: {e}")

            if self.check_html.isChecked():
                output_path = os.path.join(output_dir, f"{base_name}.html")
                HTMLExporter.export(slides, "Presentation", output_path, template)
                exported.append(output_path)

            QMessageBox.information(
                self, "Success",
                f"Exported {len(slides)} slides!\n\nSaved to Documents:\n" +
                "\n".join([os.path.basename(f) for f in exported])
            )

        except Exception as e:
            QMessageBox.critical(self, "Export Error", f"Failed to export: {e}")

    def _toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self._apply_theme()
    
    def _apply_theme(self):
        if self.dark_mode:
            dark_stylesheet = """
                QMainWindow { background-color: #1E1E2E; }
                QWidget { background-color: #1E1E2E; color: #E0E0E0; }
                QGroupBox { 
                    border: 1px solid #333; 
                    border-radius: 8px;
                    padding: 10px;
                    background-color: #252535;
                    margin-top: 10px;
                }
                QGroupBox::title { color: #E0E0E0; }
                QLineEdit, QTextEdit { 
                    background-color: #2D2D3D; 
                    color: #E0E0E0;
                    border: 1px solid #444;
                    border-radius: 5px;
                    padding: 8px;
                }
                QPushButton { 
                    background-color: #3D3D4D; 
                    color: #E0E0E0;
                    border: none;
                    border-radius: 5px;
                    padding: 8px 16px;
                }
                QPushButton:hover { background-color: #4D4D5D; }
                QTabWidget::pane { border: 1px solid #333; background-color: #252535; }
                QTabBar::tab { 
                    background-color: #2D2D3D; 
                    color: #AAA;
                    padding: 8px 16px;
                    border: none;
                }
                QTabBar::tab:selected { background-color: #3D3D4D; color: #FFF; }
                QListWidget { 
                    background-color: #2D2D3D; 
                    color: #E0E0E0;
                    border: 1px solid #333;
                }
                QComboBox { 
                    background-color: #2D2D3D; 
                    color: #E0E0E0;
                    border: 1px solid #444;
                    padding: 5px;
                }
                QCheckBox { color: #E0E0E0; }
                QLabel { color: #E0E0E0; }
                QProgressBar { 
                    background-color: #2D2D3D; 
                    border: 1px solid #333;
                }
                QProgressBar::chunk { background-color: #4A90D9; }
            """
            self.setStyleSheet(dark_stylesheet)
            self.setWindowTitle("Slidr - AI Presentation Maker v2.4 🌙")
        else:
            light_stylesheet = """
                QMainWindow { background-color: #F5F5F5; }
                QWidget { background-color: #F5F5F5; color: #1A1A1A; }
                QGroupBox { 
                    border: 1px solid #DDD; 
                    border-radius: 8px;
                    padding: 10px;
                    background-color: #FFF;
                    margin-top: 10px;
                }
                QGroupBox::title { color: #333; }
                QLineEdit, QTextEdit { 
                    background-color: #FFF; 
                    color: #1A1A1A;
                    border: 1px solid #CCC;
                    border-radius: 5px;
                    padding: 8px;
                }
                QPushButton { 
                    background-color: #4A90D9; 
                    color: #FFF;
                    border: none;
                    border-radius: 5px;
                    padding: 8px 16px;
                }
                QPushButton:hover { background-color: #357ABD; }
                QTabWidget::pane { border: 1px solid #DDD; background-color: #FFF; }
                QTabBar::tab { 
                    background-color: #E0E0E0; 
                    color: #666;
                    padding: 8px 16px;
                    border: none;
                }
                QTabBar::tab:selected { background-color: #4A90D9; color: #FFF; }
                QListWidget { 
                    background-color: #FFF; 
                    color: #1A1A1A;
                    border: 1px solid #DDD;
                }
                QComboBox { 
                    background-color: #FFF; 
                    color: #1A1A1A;
                    border: 1px solid #CCC;
                    padding: 5px;
                }
                QCheckBox { color: #333; }
                QLabel { color: #333; }
                QProgressBar { 
                    background-color: #E0E0E0; 
                    border: 1px solid #CCC;
                }
                QProgressBar::chunk { background-color: #4A90D9; }
            """
            self.setStyleSheet(light_stylesheet)
            self.setWindowTitle("Slidr - AI Presentation Maker v2.4 ☀️")


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    window = SlidrWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()