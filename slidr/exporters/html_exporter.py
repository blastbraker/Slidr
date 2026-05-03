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
        body {{ font-family: 'Segoe UI', Arial, sans-serif; }}
        .slide {{ display: none; width: 100vw; min-height: 100vh; padding: 50px; }}
        .slide.active {{ display: block; }}
        
        .slide.title {{ background: {bg_color}; color: {title_color}; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; }}
        .slide.content {{ background: {bg_color}; color: {title_color}; }}
        .slide.divider {{ background: {accent_color}; color: #fff; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; }}
        .slide.bullets_image {{ background: {bg_color}; color: {title_color}; display: flex; gap: 30px; }}
        .slide.two_column {{ background: {bg_color}; color: {title_color}; display: flex; gap: 30px; }}
        
        .slide h1 {{ font-size: 2.2rem; margin-bottom: 15px; }}
        .slide .subtitle {{ font-size: 1.3rem; opacity: 0.7; margin-bottom: 25px; }}
        .slide ul {{ font-size: 1.2rem; line-height: 1.7; list-style: none; }}
        .slide ul li {{ margin: 10px 0; padding-left: 20px; position: relative; }}
        .slide ul li:before {{ content: '•'; position: absolute; left: 0; color: {accent_color}; }}
        .image-box {{ width: 48%; background: #444; border-radius: 8px; display: flex; align-items: center; justify-content: center; color: #aaa; font-size: 1rem; }}
        .left-col, .right-col {{ width: 45%; }}
        
        @keyframes fadeIn {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}
        .slide.active {{ animation: fadeIn 0.3s ease-out; }}
    </style>
</head>
<body>
{slides}
    <script>
        let current = 0;
        const slides = document.querySelectorAll('.slide');
        slides[current].classList.add('active');

        document.addEventListener('keydown', function(e) {{
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
    "minimal": {"title_color": "#1E3A5F", "accent_color": "#E74C3C", "bg_color": "#F5F5F5"},
    "modern": {"title_color": "#FFFFFF", "accent_color": "#E94560", "bg_color": "#1A1A2E"},
    "corporate": {"title_color": "#FFFFFF", "accent_color": "#27AE60", "bg_color": "#2C3E50"},
}


def build_slide_html(slide_data: Dict[str, Any], i: int) -> str:
    slide_type = slide_data.get("type", "content")
    title_text = slide_data.get("title", f"Slide {i+1}")
    subtitle = slide_data.get("subtitle", "")
    bullets = slide_data.get("bullets", [])
    image_kw = slide_data.get("image_keywords", "")
    
    bullets_html = "".join([f"<li>{b}</li>" for b in bullets])
    
    if slide_type == "title":
        html = '<div class="slide title">'
        html += f'<h1>{title_text}</h1>'
        if subtitle:
            html += f'<div class="subtitle">{subtitle}</div>'
        html += '</div>'
    
    elif slide_type == "divider":
        html = '<div class="slide divider">'
        html += f'<h1>{title_text}</h1>'
        if subtitle:
            html += f'<div class="subtitle">{subtitle}</div>'
        html += '</div>'
    
    elif slide_type == "bullets_image":
        left_bullets = bullets[:4] if bullets else ["Point 1", "Point 2"]
        left_html = "".join([f"<li>{b}</li>" for b in left_bullets])
        html = '<div class="slide bullets_image">'
        html += f'<div class="left-col"><h1>{title_text}</h1><ul>{left_html}</ul></div>'
        html += f'<div class="image-box">📷 {image_kw or "image"}</div>'
        html += '</div>'
    
    elif slide_type == "two_column":
        left_bullets = bullets[:3] if bullets else ["Point 1", "Point 2"]
        right_bullets = bullets[3:] if len(bullets) > 3 else ["Point 4", "Point 5"]
        left_html = "".join([f"<li>{b}</li>" for b in left_bullets])
        right_html = "".join([f"<li>{b}</li>" for b in right_bullets]) if right_bullets else "<li>Additional</li>"
        html = '<div class="slide two_column">'
        html += f'<div class="left-col"><h1>{title_text}</h1><ul>{left_html}</ul></div>'
        html += f'<div class="right-col"><ul>{right_html}</ul></div>'
        html += '</div>'
    
    else:  # content
        html = '<div class="slide content">'
        html += f'<h1>{title_text}</h1>'
        if subtitle:
            html += f'<div class="subtitle">{subtitle}</div>'
        html += f'<ul>{bullets_html}</ul>'
        html += '</div>'
    
    return html


class HTMLExporter:
    @staticmethod
    def export(
        slides: List[Dict[str, Any]],
        title: str,
        output_path: str,
        theme: str = "minimal"
    ):
        theme_config = THEMES.get(theme, THEMES["minimal"])

        slides_html = ""
        for i, slide_data in enumerate(slides):
            slides_html += build_slide_html(slide_data, i)

        html = HTML_TEMPLATE.format(
            title=title,
            title_color=theme_config["title_color"],
            accent_color=theme_config["accent_color"],
            bg_color=theme_config["bg_color"],
            slides=slides_html
        )

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)

        return output_path


if __name__ == "__main__":
    print("HTMLExporter loaded")