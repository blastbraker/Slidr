# Slidr - AI Presentation Maker

## Project Overview

**Slidr** is an AI-powered desktop application that creates presentations from topics or documents. Built with Python and PySide6.

- **GitHub**: https://github.com/blastbraker/Slidr
- **License**: MIT
- **Current Version**: v3.0

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
│   ├── gui.py              # Main PySide6 GUI application v3
│   ├── config.py           # Configuration + 10 slide types
│   ├── image_search.py     # Unsplash image search integration
│   ├── processors/
│   │   └── file_processor.py   # PDF/DOCX text extraction
│   ├── generator/
│   │   └── ai_client.py      # Ollama AI client v3 (auto-layout)
│   ├── templates/
│   │   └── builder.py        # PPTX template builder v3 (10 layouts)
│   └── exporters/
│       ├── pptx_exporter.py
│       ├── pdf_exporter.py
│       └── html_exporter.py  # v3 with all layouts
├── templates/              # Built-in templates (future)
├── .gitignore
├── README.md
├── CONTRIBUTING.md
├── LICENSE
└── requirements.txt
```

---

## Features Implemented (v3.0)

| Feature | Status |
|---------|--------|
| Topic input | ✅ |
| File input (PDF/DOCX) | ✅ |
| Ollama AI integration | ✅ |
| AI auto-selects layout type | ✅ |
| 10 Slide layouts | ✅ |
| Title slide | ✅ |
| Content slide | ✅ |
| Bullets + Image slide | ✅ |
| Two Column slide | ✅ |
| Divider slide | ✅ |
| Quote slide | ✅ |
| Statistic slide | ✅ |
| Comparison slide | ✅ |
| Timeline slide | ✅ |
| Full Image slide | ✅ |
| Rich content fields | ✅ |
| Tab-based GUI | ✅ |
| Slide editor | ✅ |
| Layout picker per slide | ✅ |
| Image keywords | ✅ |
| Image URL pasting | ✅ |
| Real image embedding (PPTX) | ✅ |
| Dark/Light theme toggle | ✅ |
| Export to PPTX | ✅ |
| Export to PDF | ✅ |
| Export to HTML | ✅ |

---

## Key Files

### `slidr/gui.py`
Main GUI application v3:
- 3 tabs: Generate, Edit Slides, Export
- Dynamic editor fields based on layout type
- Theme toggle (dark/light)

### `slidr/config.py`
Configuration with 10 slide types:
- SLIDE_TYPES dict with names and fields
- Fields required per layout

### `slidr/generator/ai_client.py`
Ollama AI client v3:
- Auto-selects best layout for content
- Generates all 10 layout types
- Rich JSON output

### `slidr/templates/builder.py`
PPTX template builder v3:
- Creates presentations with 10 layout types
- Real image embedding from URLs
- Professional styling

### `slidr/image_search.py`
Image search:
- Unsplash API integration (needs API key)
- Falls back to demo placeholders

---

## Slide Layouts

### Standard Layouts (5)
1. **title**: Title slide with subtitle
2. **content**: Title + bullets
3. **bullets_image**: Bullets + image placeholder
4. **two_column**: Two column text
5. **divider**: Section transition

### New Layouts (v3) (5)
6. **quote**: Big quote with author
7. **statistic**: Large number with label
8. **comparison**: Two-column pros/cons
9. **timeline**: Chronological events
10. **full_image**: Full-bleed image + caption

---

## Configuration

Edit `slidr/config.py`:
- `OLLAMA_BASE_URL` - Ollama server (default: http://localhost:11434)
- `OLLAMA_MODEL` - AI model (default: llama3.2:3b)
- `UNSPLASH_ACCESS_KEY` - Via environment variable

---

## Known Issues / TODO

1. ~~Image embedding~~ - ✅ Fixed in v3.0
2. ~~More layouts~~ - ✅ Fixed in v3.0 (10 layouts)
3. ~~Auto-layout selection~~ - ✅ Fixed in v3.0

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
| Image download | requests + temp files |

---

## How to Test

1. Run `python -m slidr.gui`
2. Enter a topic (e.g., "History of Artificial Intelligence")
3. Click "Generate Presentation"
4. AI auto-selects layouts (10 types available)
5. Go to "Edit Slides" tab - edit any slide
6. Change layout type - fields update dynamically
7. Go to "Export" tab - choose format and export
8. Check Documents folder for output

---

## Next Steps (v3.1 Ideas)

- [ ] Live slide preview in editor
- [ ] Charts (bar/pie) rendering
- [ ] More built-in templates
- [ ] Google Slides export
- [ ] More AI backends (OpenAI, Anthropic)
- [ ] Better image search UI with thumbnails

---

## Notes

- Project uses environment variables for API keys (never commit keys)
- GUI uses PySide6 with Fusion style
- AI calls are async via QThread to keep UI responsive
- Templates use python-pptx for generating PowerPoint files
- All slide data is JSON with standardized structure
- v3: AI picks best layout, user can override

---

**Last updated**: May 2026
**Maintainer**: Ali Bahar