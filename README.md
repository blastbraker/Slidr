# Slidr - AI Presentation Maker

Create professional presentations from topics or documents using AI. Supports PPTX, PDF, and web-based HTML output.

## Features

- **Multiple Input Methods**: Enter a topic directly or upload PDF/DOCX files
- **AI-Powered**: Generate slide content using local Ollama AI
- **Multiple Outputs**: Export to PPTX, PDF, and HTML formats
- **Custom Templates**: Choose from 3 built-in themes or use your own
- **100% Free**: Uses local Ollama AI - no API costs

## Requirements

- Python 3.8+
- Ollama (installed locally)
- AI Model: `llama3.2:3b`

## Installation

1. Install Ollama from [ollama.com](https://ollama.com)

2. Pull the AI model:
   ```bash
   ollama pull llama3.2:3b
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

```bash
python -m slidr.gui
```

## Project Structure

```
Slidr/
├── slidr/
│   ├── gui.py              # Main GUI application
│   ├── config.py          # Configuration settings
│   ├── processors/        # File extraction (PDF/DOCX)
│   ├── generator/         # AI content generation
│   ├── templates/         # Slide template system
│   └── exporters/        # PPTX, PDF, HTML exporters
└── templates/            # Built-in slide templates
```

## License

MIT License - See LICENSE file for details.