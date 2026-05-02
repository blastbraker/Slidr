"""Main GUI for Slidr - AI Presentation Maker"""

import sys
import os
from datetime import datetime
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTextEdit, QCheckBox,
    QRadioButton, QButtonGroup, QFileDialog, QMessageBox,
    QProgressBar, QGroupBox, QComboBox, QFrame
)
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QIcon, QFontDatabase
from slidr.config import TEMPLATES, OUTPUT_FORMATS, OLLAMA_MODEL
from slidr.processors import FileProcessor
from slidr.generator import AIClient
from slidr.exporters import PPTXExporter, PDFExporter, HTMLExporter


class GenerationThread(QThread):
    """Thread for generating slides in background"""
    progress = Signal(str)
    finished = Signal(list)
    error = Signal(str)

    def __init__(self, client, topic=None, file_path=None, num_slides=5):
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


class SlidrWindow(QMainWindow):
    """Main application window"""

    def __init__(self):
        super().__init__()
        self.ai_client = AIClient()
        self.generation_thread = None
        self.current_slides = []
        self.input_file = None
        self.template_radios = {}

        self.setWindowTitle("Slidr - AI Presentation Maker")
        self.setGeometry(100, 100, 800, 700)

        self._setup_ui()

    def _setup_ui(self):
        """Setup the user interface"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(30, 30, 30, 30)

        title_label = QLabel("Slidr")
        title_label.setStyleSheet("font-size: 32px; font-weight: bold; color: #4A90D9;")
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        subtitle = QLabel("AI-Powered Presentation Maker")
        subtitle.setStyleSheet("font-size: 14px; color: #666;")
        subtitle.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(subtitle)

        main_layout.addSpacing(10)

        input_group = QGroupBox("Input")
        input_group.setStyleSheet("QGroupBox { font-weight: bold; }")
        input_layout = QVBoxLayout(input_group)

        topic_label = QLabel("Topic (enter a topic or upload a file):")
        input_layout.addWidget(topic_label)

        self.topic_input = QLineEdit()
        self.topic_input.setPlaceholderText("Enter your presentation topic...")
        self.topic_input.setStyleSheet("padding: 8px; font-size: 14px;")
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

        main_layout.addWidget(input_group)

        config_group = QGroupBox("Configuration")
        config_layout = QHBoxLayout(config_group)

        layout_left = QVBoxLayout()
        layout_left.addWidget(QLabel("Output Formats:"))

        self.check_pptx = QCheckBox("PPTX (PowerPoint)")
        self.check_pptx.setChecked(True)
        layout_left.addWidget(self.check_pptx)

        self.check_pdf = QCheckBox("PDF")
        layout_left.addWidget(self.check_pdf)

        self.check_html = QCheckBox("HTML (Web)")
        layout_left.addWidget(self.check_html)

        config_layout.addLayout(layout_left)

        layout_right = QVBoxLayout()
        layout_right.addWidget(QLabel("Template:"))

        self.template_group = QButtonGroup()
        self.template_radios = {}
        i = 0
        for key, config in TEMPLATES.items():
            radio = QRadioButton(config["name"])
            radio.setToolTip(config["description"])
            if i == 0:
                radio.setChecked(True)
            self.template_group.addButton(radio)
            self.template_radios[radio] = key
            layout_right.addWidget(radio)
            i += 1

        config_layout.addLayout(layout_right)

        main_layout.addWidget(config_group)

        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet("color: #666; font-size: 12px;")
        main_layout.addWidget(self.status_label)

        generate_btn = QPushButton("Generate Presentation")
        generate_btn.setStyleSheet("""
            QPushButton {
                background-color: #4A90D9;
                color: white;
                padding: 15px;
                font-size: 16px;
                font-weight: bold;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #357ABD;
            }
            QPushButton:disabled {
                background-color: #ccc;
            }
        """)
        generate_btn.clicked.connect(self._generate)
        main_layout.addWidget(generate_btn)

        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        main_layout.addWidget(self.progress_bar)

    def _browse_file(self):
        """Browse for input file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Input File",
            "",
            "Documents (*.pdf *.docx *.doc);;PDF Files (*.pdf);;Word Documents (*.docx *.doc)"
        )

        if file_path:
            self.input_file = file_path
            self.file_input.setText(os.path.basename(file_path))
            self.topic_input.clear()

    def _generate(self):
        """Generate the presentation"""
        topic = self.topic_input.text().strip()
        file_path = self.input_file

        if not topic and not file_path:
            QMessageBox.warning(self, "Input Required", "Please enter a topic or select a file.")
            return

        if not self.check_pptx.isChecked() and not self.check_pdf.isChecked() and not self.check_html.isChecked():
            QMessageBox.warning(self, "Output Required", "Please select at least one output format.")
            return

        self.status_label.setText("Checking Ollama connection...")
        if not self.ai_client.is_available():
            QMessageBox.critical(
                self,
                "Ollama Not Available",
                "Could not connect to Ollama. Please ensure:\n"
                "1. Ollama is installed\n"
                "2. Ollama is running\n"
                "3. Model is downloaded (ollama pull llama3.2:3b)"
            )
            self.status_label.setText("Ready")
            return

        self.status_label.setText("Connecting to Ollama...")
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)

        self.generation_thread = GenerationThread(
            self.ai_client,
            topic=topic if topic else None,
            file_path=file_path,
            num_slides=5
        )
        self.generation_thread.progress.connect(self._on_progress)
        self.generation_thread.finished.connect(self._on_generated)
        self.generation_thread.error.connect(self._on_error)
        self.generation_thread.start()

    def _on_progress(self, message):
        """Handle generation progress"""
        self.status_label.setText(message)

    def _on_generated(self, slides):
        """Handle successful generation"""
        self.current_slides = slides
        self.progress_bar.setVisible(False)

        presentation_title = self.topic_input.text().strip() or os.path.splitext(self.file_input.text())[0]

        # Hardcoded Documents folder - no prompt
        output_dir = os.path.join(os.path.expanduser("~"), "Documents")

        selected_template = self.template_group.checkedButton()
        for radio, key in self.template_radios.items():
            if radio is self.template_group.checkedButton():
                template = key
                break
        else:
            template = "minimal"

        exported = []
        
        safe_title = "".join(c for c in presentation_title if c.isalnum() or c in " _-").strip()
        if not safe_title:
            safe_title = "presentation"
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_title = f"{safe_title}_{timestamp}"
        
        base_name = os.path.join(output_dir, safe_title)
        
        try:
            if self.check_pptx.isChecked():
                output_path = f"{base_name}.pptx"
                PPTXExporter.export(slides, presentation_title, output_path, template)
                exported.append(output_path)

            if self.check_pdf.isChecked():
                output_path = f"{base_name}.pdf"
                try:
                    PDFExporter.export(slides, presentation_title, output_path, template)
                    exported.append(output_path)
                except ImportError as e:
                    QMessageBox.warning(
                        self,
                        "PDF Export Warning",
                        f"Could not export PDF: {e}\nPPTX was exported."
                    )

            if self.check_html.isChecked():
                output_path = f"{base_name}.html"
                HTMLExporter.export(slides, presentation_title, output_path, template)
                exported.append(output_path)

            self.status_label.setText(f"Generated {len(exported)} file(s)")

            QMessageBox.information(
                self,
                "Success",
                f"Presentation generated successfully!\n\nSaved to Documents folder:\n" +
                "\n".join([os.path.basename(f) for f in exported])
            )

        except Exception as e:
            QMessageBox.critical(self, "Export Error", f"Failed to export: {e}")
            self.status_label.setText("Export failed")

        self.status_label.setText("Ready")

    def _on_error(self, error):
        """Handle generation error"""
        self.progress_bar.setVisible(False)
        self.status_label.setText("Error")
        QMessageBox.critical(self, "Generation Error", f"Failed to generate: {error}")


def main():
    """Launch the application"""
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    window = SlidrWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()