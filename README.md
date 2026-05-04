# Slidr - AI Presentation Maker

Create professional presentations from topics or documents using AI. Supports PPTX, PDF, and web-based HTML output.

## Features

- **10 Slide Layouts**: Including Quote, Statistic, Comparison, Timeline, and Full Image
- **AI Auto-Layout**: AI selects the best layout for each slide automatically
- **Real Image Embedding**: Images embedded directly in PPTX exports
- **Multiple Input Methods**: Enter a topic directly or upload PDF/DOCX files
- **AI-Powered**: Generate slide content using local Ollama AI
- **Multiple Outputs**: Export to PPTX, PDF, and HTML formats
- **Custom Templates**: Choose from 3 built-in themes (Minimal, Modern, Corporate)
- **100% Free**: Uses local Ollama AI - no API costs
- **Cross-Platform**: Works on Windows, macOS, and Linux

## Requirements

- Python 3.8+
- Ollama (installed locally)
- AI Model: `llama3.2:3b`

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/blastbraker/Slidr.git
cd Slidr
```

### 2. Install Ollama

Download from [ollama.com](https://ollama.com) and install for your OS.

Pull the AI model:
```bash
ollama pull llama3.2:3b
```

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Slidr

```bash
python -m slidr.gui
```

## Usage

1. **Enter a topic** in the text field OR **browse** to upload a PDF/DOCX file
2. AI auto-selects the best layout for each slide
3. Click **Generate Presentation**
4. Review slides in the **Edit Slides** tab
5. Change layout type if needed - fields update dynamically
6. Export to **PPTX**, **PDF**, or **HTML**
7. Find your presentation in the **Documents** folder

## Slide Layouts

### Standard Layouts (5)
- **Title**: Title slide with subtitle
- **Content**: Title + bullets
- **Bullets + Image**: Bullets with image placeholder
- **Two Column**: Two column text
- **Divider**: Section transition

### New in v3.0 (5)
- **Quote**: Big quote with author citation
- **Statistic**: Large number with label
- **Comparison**: Pros vs Cons two-column
- **Timeline**: Chronological events
- **Full Image**: Full-bleed image with caption

### Templates

#### Minimal Theme
Dark blue background with red accent bar - clean and modern

#### Modern Theme  
Dark purple background with pink accent - bold and creative

#### Corporate Theme
Dark gray background with green accent - professional look

## Troubleshooting

### Ollama not connecting?
- Make sure Ollama is running (`ollama serve`)
- Check the model is downloaded (`ollama list`)

### Import errors?
- Ensure all dependencies are installed: `pip install -r requirements.txt`

### PDF export not working?
- Install pdf2image with poppler: `pip install pdf2image[poppler]`

## License

MIT License - See LICENSE file for details.

## Author

Ali Bahar