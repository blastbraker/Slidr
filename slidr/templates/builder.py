"""Template builder for creating slide themes"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from typing import List, Dict, Any, Optional
from slidr.config import TEMPLATES
import os


class TemplateBuilder:
    """Build presentation templates with different themes"""

    def __init__(self, theme: str = "minimal"):
        self.theme = theme
        self.theme_config = TEMPLATES.get(theme, TEMPLATES["minimal"])

    def create_presentation(self, slides: List[Dict[str, Any]], title: str) -> Presentation:
        """Create a new presentation with the given slides"""
        prs = Presentation()
        prs.slide_width = Inches(10)
        prs.slide_height = Inches(7.5)

        title_slide = prs.slides.add_slide(prs.slide_layouts[6])
        self._apply_title_slide(title_slide, title)

        for i, slide_data in enumerate(slides):
            content_slide = prs.slides.add_slide(prs.slide_layouts[6])
            self._apply_content_slide(content_slide, slide_data, i)

        return prs

    def _apply_title_slide(self, slide, title: str):
        """Apply title slide styling"""
        shapes = slide.shapes
        title_box = shapes.add_textbox(Inches(1), Inches(2.5), Inches(8), Inches(1.5))
        tf = title_box.text_frame
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(44)
        p.font.bold = True
        p.alignment = PP_ALIGN.CENTER

        config = self.theme_config
        if config["primary_color"] == "FFFFFF":
            p.font.color.rgb = RGBColor(0, 0, 0)
        else:
            p.font.color.rgb = RGBColor(255, 255, 255)

        background = shapes.add_shape(1, Inches(0), Inches(0), Inches(10), Inches(7.5))
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = self._hex_to_rgb(config["primary_color"])
        background.line.fill.background()

    def _apply_content_slide(self, slide, data: Dict[str, Any], index: int):
        """Apply content slide styling"""
        shapes = slide.shapes

        title_box = shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(9), Inches(0.8))
        tf = title_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = data.get("title", f"Slide {index + 1}")
        p.font.size = Pt(32)
        p.font.bold = True

        config = self.theme_config
        if config["primary_color"] == "FFFFFF":
            p.font.color.rgb = RGBColor(0, 0, 0)
        else:
            p.font.color.rgb = RGBColor(255, 255, 255)

        bullet_box = shapes.add_textbox(Inches(0.7), Inches(1.3), Inches(8.5), Inches(5))
        tf = bullet_box.text_frame

        bullets = data.get("bullets", [])
        for i, bullet in enumerate(bullets):
            if i == 0:
                p = tf.paragraphs[0]
            else:
                p = tf.add_paragraph()
            p.text = bullet
            p.font.size = Pt(20)
            p.level = 0

            if config["primary_color"] == "FFFFFF":
                p.font.color.rgb = RGBColor(0, 0, 0)
            else:
                p.font.color.rgb = RGBColor(200, 200, 200)

        if config.get("accent_color"):
            accent_bar = shapes.add_shape(1, Inches(0), Inches(0), Inches(0.15), Inches(7.5))
            fill = accent_bar.fill
            fill.solid()
            fill.fore_color.rgb = self._hex_to_rgb(config["accent_color"])
            accent_bar.line.fill.background()

    def _hex_to_rgb(self, hex_color: str):
        """Convert hex color to RGB"""
        hex_color = hex_color.lstrip("#")
        return RGBColor(
            int(hex_color[0:2], 16),
            int(hex_color[2:4], 16),
            int(hex_color[4:6], 16)
        )

    def load_template(self, template_path: str) -> Presentation:
        """Load a custom PPTX as template"""
        if not os.path.exists(template_path):
            raise FileNotFoundError(f"Template not found: {template_path}")
        return Presentation(template_path)


def create_from_template(
    slides: List[Dict[str, Any]],
    title: str,
    theme: str = "minimal",
    template_path: Optional[str] = None
) -> Presentation:
    """Create presentation from theme or custom template"""
    if template_path and os.path.exists(template_path):
        prs = Presentation(template_path)
    else:
        builder = TemplateBuilder(theme)
        prs = builder.create_presentation(slides, title)
    return prs


def main():
    """Test template builder"""
    test_slides = [
        {"title": "Introduction", "bullets": ["Welcome", "Overview of topics"], "notes": ""},
        {"title": "Key Points", "bullets": ["Point 1", "Point 2", "Point 3"], "notes": ""},
        {"title": "Conclusion", "bullets": ["Summary", "Next steps"], "notes": ""},
    ]

    for theme in ["minimal", "modern", "corporate"]:
        builder = TemplateBuilder(theme)
        print(f"Theme '{theme}': {builder.theme_config['name']}")


if __name__ == "__main__":
    main()