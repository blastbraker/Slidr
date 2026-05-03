# Slidr - AI Presentation Maker

## Project Overview

**Slidr** is an AI-powered desktop application that creates presentations from topics or documents. Built with Python and PySide6.

- **GitHub**: https://github.com/blastbraker/Slidr
- **License**: MIT
- **Current Version**: v2.x

---

## Quick Start

```bash
# Clone
git clone https://github.com/blastbraker/Slidr.git
cd Slidr

# Install dependencies
pip install -r requirements.txt

# Run
python -m slidr.gui
```

### For Image Search (Optional)

Set Unsplash API key (not committed to git):
```powershell
$env:UNSPLASH_ACCESS_KEY = "your_key_here"
python -m slidr.gui
```

---

## Project Structure

```
Slidr/
├── slidr/
│   ├── gui.py              # Main PySide6 GUI application
│   ├── config.py           # Configuration (OLLAMA_BASE_URL, UNSPLASH_ACCESS_KEY)
│   ├── image_search.py     # Unsplash image search integration
│   ├── processors/
│   │   └── file_processor.py   # PDF/DOCX text extraction
│   ├── generator/
│   │   └── ai_client.py      # Ollama AI client
│   ├── templates/
│   │   └── builder.py        # PPTX template builder with 5 layouts
│   └── exporters/
│       ├── pptx_exporter.py
│       ├── pdf_exporter.py
│       └── html_exporter.py
├── templates/              # Built-in templates (future)
├── .gitignore
├── README.md
├── CONTRIBUTING.md
├── LICENSE
└── requirements.txt
```

---

## Features Implemented (v2)

| Feature | Status |
|---------|--------|
| Topic input | ✅ |
| File input (PDF/DOCX) | ✅ |
| Ollama AI integration | ✅ |
| 5 Slide layouts | ✅ |
| - title | ✅ |
| - content | ✅ |
| - bullets_image | ✅ |
| - two_column | ✅ |
| - divider | ✅ |
| Rich content (title, subtitle, bullets, notes) | ✅ |
| Tab-based GUI | ✅ |
| Slide editor | ✅ |
| Layout picker per slide | ✅ |
| Image keywords | ✅ |
| Image URL pasting | ✅ |
| Dark/Light theme toggle | ✅ |
| Export to PPTX | ✅ |
| Export to PDF | ✅ |
| Export to HTML | ✅ |

---

## Key Files

### `slidr/gui.py`
Main GUI application with:
- 3 tabs: Generate, Edit Slides, Export
- Theme toggle (dark/light)
- Slide list and editor
- Export functionality

### `slidr/generator/ai_client.py`
Ollama AI client:
- Generates slides from topic or text
- Rich JSON output with type, title, subtitle, bullets, image_keywords
- 5 slide types: title, content, bullets_image, two_column, divider

### `slidr/templates/builder.py`
PPTX template builder:
- Creates presentations with 5 layout types
- Professional styling with themes (minimal, modern, corporate)
- Image placeholders

### `slidr/image_search.py`
Image search:
- Unsplash API integration (needs API key)
- Falls back to demo placeholders

---

## Configuration

Edit `slidr/config.py`:
- `OLLAMA_BASE_URL` - Ollama server (default: http://localhost:11434)
- `OLLAMA_MODEL` - AI model (default: llama3.2:3b)
- `UNSPLASH_ACCESS_KEY` - Via environment variable

---

## Known Issues / TODO

1. **Image embedding** - Currently shows text placeholders; real images not embedded in PPTX
2. **Live preview** - No real-time slide preview in GUI
3. **More templates** - Only 3 basic themes
4. **Image search** - Needs API key for real Unsplash results

---

## Technology Stack

| Component | Technology |
|-----------|-----------|
| GUI | PySide6 |
| AI | Ollama (llama3.2:3b) |
| PPTX | python-pptx |
| PDF | python-pptx + pdf2image |
| HTML | Custom HTML/JS |
| File processing | PyMuPDF, python-docx |
| HTTP | requests |

---

## How to Test

1. Run `python -m slidr.gui`
2. Enter a topic (e.g., "History of Artificial Intelligence")
3. Click "Generate Presentation"
4. Go to "Edit Slides" tab - edit any slide
5. Go to "Export" tab - choose format and export
6. Check Documents folder for output

---

## Next Steps (v3 Ideas)

- [ ] Embed real images in PPTX
- [ ] Live slide preview
- [ ] More built-in templates
- [ ] Google Slides export
- [ ] More AI backends (OpenAI, Anthropic)
- [ ] Better image search UI with thumbnails

---

## Notes for Next AI

- The project uses environment variables for API keys (never commit keys)
- GUI uses PySide6 with Fusion style
- AI calls are async via QThread to keep UI responsive
- Templates use python-pptx for generating PowerPoint files
- All slide data is JSON with standardized structure

---

**Last updated**: May 2026
**Maintainer**: Ali Bahar
