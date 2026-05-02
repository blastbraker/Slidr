"""HTML exporter for creating web-based presentations"""

import os
from typing import List, Dict, Any, Optional


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', Arial, sans-serif; background: #1a1a1a; color: #fff; }}
        .slide {{ display: none; width: 100vw; height: 100vh; padding: 60px; justify-content: center; align-items: center; flex-direction: column; }}
        .slide.active {{ display: flex; }}
        .slide h1 {{ font-size: 3rem; margin-bottom: 40px; text-align: center; color: {title_color}; }}
        .slide ul {{ font-size: 1.5rem; max-width: 800px; line-height: 1.8; list-style: none; }}
        .slide ul li {{ margin: 15px 0; padding-left: 30px; position: relative; }}
        .slide ul li:before {{ content: '•'; position: absolute; left: 0; color: {accent_color}; }}
        @keyframes fadeIn {{ from {{ opacity: 0; transform: translateY(20px); }} to {{ opacity: 1; transform: translateY(0); }} }}
        .slide.active {{ animation: fadeIn 0.5s ease-out; }}
    </style>
</head>
<body>
{slides}
    <script>
        let current = 0;
        const slides = document.querySelectorAll('.slide');
        slides[current].classList.add('active');

        document.addEventListener('keydown', (e) => {{
            if (e.key === 'ArrowRight' || e.key === ' ') {{
                slides[current].classList.remove('active');
                current = (current + 1) % slides.length;
                slides[current].classList.add('active');
            }} else if (e.key === 'ArrowLeft') {{
                slides[current].classList.remove('active');
                current = (current - 1 + slides.length) % slides.length;
                slides[current].classList.add('active');
            }}
        }});
    </script>
</body>
</html>"""


THEMES = {
    "minimal": {"title_color": "#000000", "accent_color": "#4A90D9", "bg_color": "#FFFFFF"},
    "modern": {"title_color": "#FFFFFF", "accent_color": "#4A90D9", "bg_color": "#1E1E1E"},
    "corporate": {"title_color": "#FFFFFF", "accent_color": "#3498DB", "bg_color": "#2C3E50"},
}


class HTMLExporter:
    """Export presentation to HTML/JS slides"""

    @staticmethod
    def export(
        slides: List[Dict[str, Any]],
        title: str,
        output_path: str,
        theme: str = "minimal"
    ):
        """Export slides to HTML file"""
        theme_config = THEMES.get(theme, THEMES["minimal"])

        slides_html = ""
        for i, slide_data in enumerate(slides):
            bullets = "".join([f"<li>{b}</li>" for b in slide_data.get("bullets", [])])
            slides_html += f'<div class="slide"><h1>{slide_data.get("title", f"Slide {i+1}")}</h1><ul>{bullets}</ul></div>'

        html = HTML_TEMPLATE.format(
            title=title,
            title_color=theme_config["title_color"],
            accent_color=theme_config["accent_color"],
            slides=slides_html
        )

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)

        return output_path


def main():
    """Test HTML export"""
    test_slides = [
        {"title": "Introduction", "bullets": ["Welcome to Slidr", "AI-powered presentations"]},
        {"title": "How It Works", "bullets": ["Enter topic or upload file", "AI generates content", "Export to multiple formats"]},
    ]
    print("HTMLExporter loaded")


if __name__ == "__main__":
    main()