"""Main GUI for Slidr - AI Presentation Maker v3"""

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
from slidr.config import TEMPLATES, SLIDE_TYPES


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
                from slidr.processors import FileProcessor
                text = FileProcessor.extract_text(self.file_path)
                slides = self.client.generate_from_text(text, self.num_slides)
            else:
                slides = self.client.generate_slides(self.topic, self.num_slides)
            self.progress.emit("Done")
            self.finished.emit(slides)
        except Exception as e:
            self.error.emit(str(e))


class SlideEditorWidget(QWidget):
    """Widget for editing a single slide with dynamic fields based on layout type"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.slide_data = {}
        self.field_widgets = {}
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        
        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel("Layout:"))
        self.type_combo = QComboBox()
        for t, desc in SLIDE_TYPES.items():
            self.type_combo.addItem(desc["name"], t)
        self.type_combo.currentIndexChanged.connect(self._on_type_changed)
        type_layout.addWidget(self.type_combo)
        
        self.ai_suggested_label = QLabel("🤖 AI suggested")
        self.ai_suggested_label.setStyleSheet("color: #4A90D9; font-size: 11px;")
        type_layout.addWidget(self.ai_suggested_label)
        type_layout.addStretch()
        layout.addLayout(type_layout)
        
        self.fields_container = QWidget()
        self.fields_layout = QVBoxLayout(self.fields_container)
        self.fields_layout.setSpacing(8)
        layout.addWidget(self.fields_container)
        
        self._build_fields("content")
        
        layout.addStretch()
    
    def _build_fields(self, slide_type: str):
        while self.fields_layout.count():
            item = self.fields_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        self.field_widgets = {}
        
        if slide_type in ("title", "content", "divider", "two_column"):
            self._add_field("Title", "title_edit", QLineEdit(), "Slide title...")
            self._add_field("Subtitle", "subtitle_edit", QLineEdit(), "Optional subtitle...")
            
        if slide_type in ("content", "bullets_image", "two_column"):
            self._add_field("Bullet Points", "bullets_edit", QTextEdit(), "One bullet per line...", height=100)
            
        if slide_type == "quote":
            self._add_field("Quote", "quote_edit", QTextEdit(), "The quote text...", height=80)
            self._add_field("Author", "author_edit", QLineEdit(), "Author name...")
            
        if slide_type == "statistic":
            self._add_field("Big Number", "big_number_edit", QLineEdit(), "e.g., 85%, $1B, 3x")
            self._add_field("Label", "stat_label_edit", QLineEdit(), "e.g., Growth, Revenue")
            self._add_field("Context", "subtitle_edit", QLineEdit(), "Additional context...")
            
        if slide_type == "comparison":
            self._add_field("Title", "title_edit", QLineEdit(), "Slide title...")
            self._add_field("Left Column Title", "left_title_edit", QLineEdit(), "e.g., Pros")
            self._add_field("Left Items", "left_items_edit", QTextEdit(), "One per line...", height=80)
            self._add_field("Right Column Title", "right_title_edit", QLineEdit(), "e.g., Cons")
            self._add_field("Right Items", "right_items_edit", QTextEdit(), "One per line...", height=80)
            
        if slide_type == "timeline":
            self._add_field("Title", "title_edit", QLineEdit(), "Slide title...")
            self._add_field("Events", "events_edit", QTextEdit(), "Format: YYYY - Event name\nOne per line...", height=100)
            
        if slide_type == "full_image":
            self._add_field("Overlay Title", "overlay_title_edit", QLineEdit(), "Title over image...")
            self._add_field("Caption", "caption_edit", QLineEdit(), "Image caption...")
            
        if slide_type in ("title", "content", "bullets_image", "two_column", "quote", "comparison", "timeline", "full_image"):
            self._add_field("Image Keywords", "image_keywords_edit", QLineEdit(), "Keywords for image search...")
            
            image_layout = QHBoxLayout()
            self.field_widgets["image_url_edit"] = self.field_widgets.get("image_keywords_edit")
            self.search_image_btn = QPushButton("Search")
            self.search_image_btn.setStyleSheet("padding: 5px 10px;")
            image_layout.addWidget(self.search_image_btn)
            self.fields_layout.addLayout(image_layout)
    
    def _add_field(self, label: str, key: str, widget, placeholder: str = "", height: int = 0):
        self.fields_layout.addWidget(QLabel(label))
        if isinstance(widget, QLineEdit):
            widget.setPlaceholderText(placeholder)
        elif isinstance(widget, QTextEdit):
            widget.setPlaceholderText(placeholder)
            if height > 0:
                widget.setMaximumHeight(height)
        self.fields_layout.addWidget(widget)
        self.field_widgets[key] = widget
    
    def _on_type_changed(self, index):
        slide_type = self.type_combo.currentData()
        self._build_fields(slide_type)
    
    def load_slide(self, slide_data: dict):
        self.slide_data = slide_data
        slide_type = slide_data.get("type", "content")
        
        for i in range(self.type_combo.count()):
            if self.type_combo.itemData(i) == slide_type:
                self.type_combo.setCurrentIndex(i)
                break
        
        self.ai_suggested_label.setVisible(False)
        self.ai_suggested_label.setText("🤖 AI suggested")
        
        self._build_fields(slide_type)
        
        self._set_field("title_edit", "title", slide_data)
        self._set_field("subtitle_edit", "subtitle", slide_data)
        self._set_field("bullets_edit", "bullets", slide_data, is_list=True)
        self._set_field("quote_edit", "quote", slide_data)
        self._set_field("author_edit", "author", slide_data)
        self._set_field("big_number_edit", "big_number", slide_data)
        self._set_field("stat_label_edit", "stat_label", slide_data)
        self._set_field("left_title_edit", "left_title", slide_data)
        self._set_field("left_items_edit", "left_items", slide_data, is_list=True)
        self._set_field("right_title_edit", "right_title", slide_data)
        self._set_field("right_items_edit", "right_items", slide_data, is_list=True)
        self._set_field("events_edit", "events", slide_data, is_events=True)
        self._set_field("caption_edit", "caption", slide_data)
        self._set_field("overlay_title_edit", "overlay_title", slide_data)
        self._set_field("image_keywords_edit", "image_keywords", slide_data)
        
        image_url = slide_data.get("image_url", "")
        if image_url and "image_keywords_edit" in self.field_widgets:
            self.field_widgets["image_keywords_edit"].setText(image_url)
    
    def _set_field(self, widget_key: str, data_key: str, slide_data: dict, is_list: bool = False, is_events: bool = False):
        if widget_key not in self.field_widgets:
            return
        widget = self.field_widgets[widget_key]
        
        if is_events:
            events = slide_data.get("events", [])
            if events:
                lines = []
                for e in events:
                    if isinstance(e, dict):
                        date = e.get("date", "")
                        title = e.get("title", "")
                        lines.append(f"{date} - {title}" if date else title)
                    else:
                        lines.append(str(e))
                widget.setText("\n".join(lines))
        elif is_list:
            items = slide_data.get(data_key, [])
            if items:
                lines = [str(i) for i in items]
                widget.setText("\n".join(lines))
        else:
            value = slide_data.get(data_key, "")
            if isinstance(widget, QTextEdit):
                widget.setText(value)
            else:
                widget.setText(value)
    
    def get_slide_data(self) -> dict:
        slide_type = self.type_combo.currentData()
        
        data = {
            "type": slide_type,
            "title": self._get_field("title_edit"),
            "subtitle": self._get_field("subtitle_edit"),
            "notes": self.slide_data.get("notes", "")
        }
        
        if slide_type in ("content", "bullets_image", "two_column"):
            data["bullets"] = self._get_field_list("bullets_edit")
            
        elif slide_type == "quote":
            data["quote"] = self._get_field("quote_edit")
            data["author"] = self._get_field("author_edit")
            
        elif slide_type == "statistic":
            data["big_number"] = self._get_field("big_number_edit")
            data["stat_label"] = self._get_field("stat_label_edit")
            
        elif slide_type == "comparison":
            data["left_title"] = self._get_field("left_title_edit")
            data["left_items"] = self._get_field_list("left_items_edit")
            data["right_title"] = self._get_field("right_title_edit")
            data["right_items"] = self._get_field_list("right_items_edit")
            
        elif slide_type == "timeline":
            events_text = self._get_field("events_edit")
            events = []
            for line in events_text.split("\n"):
                line = line.strip()
                if line:
                    if " - " in line:
                        parts = line.split(" - ", 1)
                        events.append({"date": parts[0].strip(), "title": parts[1].strip()})
                    else:
                        events.append({"date": "", "title": line})
            data["events"] = events
            
        elif slide_type == "full_image":
            data["overlay_title"] = self._get_field("overlay_title_edit")
            data["caption"] = self._get_field("caption_edit")
            
        if slide_type in ("title", "content", "bullets_image", "two_column", "quote", "comparison", "timeline", "full_image"):
            img_kw = self._get_field("image_keywords_edit")
            if img_kw and "http" in img_kw:
                data["image_url"] = img_kw
            else:
                data["image_keywords"] = img_kw
        
        return data
    
    def _get_field(self, key: str) -> str:
        if key not in self.field_widgets:
            return ""
        widget = self.field_widgets[key]
        if isinstance(widget, QTextEdit):
            return widget.toPlainText()
        return widget.text()
    
    def _get_field_list(self, key: str) -> list:
        text = self._get_field(key)
        return [b.strip() for b in text.split("\n") if b.strip()]


class SlidrWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        from slidr.generator import AIClient
        from slidr.image_search import ImageSearch
        self.ai_client = AIClient()
        self.image_search = ImageSearch()
        self.generation_thread = None
        self.current_slides = []
        self.input_file = None
        self.edited_slides = []
        self.selected_image_url = None

        self.setWindowTitle("Slidr - AI Presentation Maker v3.0")
        self.setGeometry(100, 100, 950, 750)

        self._setup_ui()

    def _setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        
        title_label = QLabel("Slidr")
        title_label.setStyleSheet("font-size: 28px; font-weight: bold; color: #4A90D9;")
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        
        self.generate_tab = self._create_generate_tab()
        self.tabs.addTab(self.generate_tab, "Generate")
        
        self.edit_tab = self._create_edit_tab()
        self.tabs.addTab(self.edit_tab, "Edit Slides")
        
        self.export_tab = self._create_export_tab()
        self.tabs.addTab(self.export_tab, "Export")
        
        main_layout.addWidget(self.tabs)
        
        self.dark_mode = True
        self._apply_theme()
        
        theme_btn = QPushButton("🌙" if self.dark_mode else "☀️")
        theme_btn.setFixedSize(40, 40)
        theme_btn.setStyleSheet("font-size: 18px; border: none; background: transparent;")
        theme_btn.clicked.connect(self._toggle_theme)
        main_layout.addWidget(theme_btn, 0, Qt.AlignRight)

    def _create_generate_tab(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(15)
        
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
        
        count_layout = QHBoxLayout()
        count_layout.addWidget(QLabel("Number of slides:"))
        self.slide_count_combo = QComboBox()
        for i in range(4, 13):
            self.slide_count_combo.addItem(str(i), i)
        self.slide_count_combo.setCurrentIndex(2)
        count_layout.addWidget(self.slide_count_combo)
        count_layout.addStretch()
        input_layout.addLayout(count_layout)
        
        layout.addWidget(input_group)
        
        generate_btn = QPushButton("Generate Presentation")
        generate_btn.setStyleSheet("""
            QPushButton { background-color: #4A90D9; color: white; padding: 12px;
                font-size: 16px; font-weight: bold; border: none; border-radius: 5px; }
            QPushButton:hover { background-color: #357ABD; }
        """)
        generate_btn.clicked.connect(self._generate)
        layout.addWidget(generate_btn)
        
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
        
        left_panel = QFrame()
        left_panel.setFrameStyle(QFrame.StyledPanel)
        left_layout = QVBoxLayout(left_panel)
        
        left_layout.addWidget(QLabel("Slides:"))
        
        self.slide_list = QListWidget()
        self.slide_list.itemClicked.connect(self._on_slide_selected)
        left_layout.addWidget(self.slide_list)
        
        layout.addWidget(left_panel, 1)
        
        right_panel = QFrame()
        right_panel.setFrameStyle(QFrame.StyledPanel)
        right_layout = QVBoxLayout(right_panel)
        
        right_layout.addWidget(QLabel("Edit Slide:"))
        
        self.slide_editor = SlideEditorWidget()
        right_layout.addWidget(self.slide_editor)
        
        save_btn = QPushButton("Save Changes")
        save_btn.clicked.connect(self._save_slide)
        right_layout.addWidget(save_btn)
        
        layout.addWidget(right_panel, 2)
        
        layout.setStretchFactor(left_panel, 1)
        layout.setStretchFactor(right_panel, 2)
        
        return widget

    def _create_export_tab(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(15)
        
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
        
        first_radio = list(self.template_radios.keys())[0]
        first_radio.setChecked(True)
        
        layout.addWidget(template_group)
        
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
        
        self.slide_list.clear()
        for i, slide in enumerate(slides):
            slide_type = slide.get("type", "content")
            title = slide.get("title", f"Slide {i+1}")
            self.slide_list.addItem(f"[{slide_type}] {title}")
        
        type_counts = {}
        for s in slides:
            t = s.get("type", "content")
            type_counts[t] = type_counts.get(t, 0) + 1
        
        type_summary = ", ".join([f"{v} {k}" for k, v in type_counts.items()])
        self.status_label.setText(f"Generated {len(slides)} slides: {type_summary}")
        
        self.tabs.setCurrentIndex(1)
        
        if slides:
            self.slide_list.setCurrentRow(0)
            self._on_slide_selected(self.slide_list.currentItem())

    def _on_error(self, error):
        self.progress_bar.setVisible(False)
        self.status_label.setText("Error")
        QMessageBox.critical(self, "Generation Error", f"Failed to generate: {error}")

    def _on_slide_selected(self, item):
        row = self.slide_list.row(item)
        if row < len(self.edited_slides):
            slide = self.edited_slides[row]
            self.slide_editor.load_slide(slide)

    def _save_slide(self):
        current_row = self.slide_list.currentRow()
        if current_row < len(self.edited_slides):
            slide_data = self.slide_editor.get_slide_data()
            
            img_kw = slide_data.get("image_keywords", "")
            if img_kw and "http" in img_kw:
                slide_data["image_url"] = img_kw
            
            self.edited_slides[current_row] = slide_data
            
            slide = self.edited_slides[current_row]
            slide_type = slide.get("type", "content")
            title = slide.get("title", f"Slide {current_row+1}")
            
            img_indicator = " 📷" if slide.get("image_url") else ""
            self.slide_list.currentItem().setText(f"[{slide_type}] {title}{img_indicator}")
            
            QMessageBox.information(self, "Saved", "Slide changes saved!")

    def _export(self):
        if not self.edited_slides:
            QMessageBox.warning(self, "No Slides", "Please generate slides first.")
            return

        slides = self.edited_slides
        
        template = "minimal"
        for radio, key in self.template_radios.items():
            if radio.isChecked():
                template = key
                break
        
        base_name = f"presentation_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        output_dir = os.path.join(os.path.expanduser("~"), "Documents")
        
        exported = []
        
        try:
            from slidr.exporters import PPTXExporter, PDFExporter, HTMLExporter
            
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
            self.setWindowTitle("Slidr - AI Presentation Maker v3.0 🌙")
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
            self.setWindowTitle("Slidr - AI Presentation Maker v3.0 ☀️")


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    window = SlidrWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()