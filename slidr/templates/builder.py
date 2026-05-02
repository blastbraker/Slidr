"""Template builder for creating professional slide themes"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from typing import List, Dict, Any, Optional
from slidr.config import TEMPLATES
import os


class TemplateBuilder:
    """Simple but professional templates"""

    def __init__(self, theme: str = "minimal"):
        self.theme = theme
        self.theme_config = TEMPLATES.get(theme, TEMPLATES["minimal"])

    def create_presentation(self, slides: List[Dict[str, Any]], title: str) -> Presentation:
        prs = Presentation()
        prs.slide_width = Inches(13.333)
        prs.slide_height = Inches(7.5)

        title_slide = prs.slides.add_slide(prs.slide_layouts[6])
        self._apply_title_slide(title_slide, title)

        for i, slide_data in enumerate(slides):
            content_slide = prs.slides.add_slide(prs.slide_layouts[6])
            self._apply_content_slide(content_slide, slide_data, i)

        return prs

    def _hex_to_rgb(self, hex_color: str) -> RGBColor:
        hex_color = hex_color.lstrip("#")
        return RGBColor(
            int(hex_color[0:2], 16),
            int(hex_color[2:4], 16),
            int(hex_color[4:6], 16)
        )

    def _apply_title_slide(self, slide, title: str):
        config = self.theme_config
        accent = self._hex_to_rgb(config["accent_color"])
        is_dark = config["primary_color"] != "FFFFFF"
        
        shapes = slide.shapes
        
        title_box = shapes.add_textbox(Inches(1), Inches(2.8), Inches(11.333), Inches(2))
        tf = title_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(52)
        p.font.bold = True
        p.alignment = PP_ALIGN.CENTER
        p.font.color.rgb = is_dark and RGBColor(255,255,255) or RGBColor(0,0,0)
        
        line = shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(4), Inches(4.6), Inches(5.333), Inches(0.06))
        line.fill.solid()
        line.fill.fore_color.rgb = accent
        line.line.fill.background()

    def _apply_content_slide(self, slide, data: Dict[str, Any], index: int):
        config = self.theme_config
        accent = self._hex_to_rgb(config["accent_color"])
        is_dark = config["primary_color"] != "FFFFFF"
        
        shapes = slide.shapes
        
        title_box = shapes.add_textbox(Inches(0.6), Inches(0.35), Inches(12), Inches(0.9))
        tf = title_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = data.get("title", f"Slide {index + 1}")
        p.font.size = Pt(32)
        p.font.bold = True
        p.font.color.rgb = is_dark and RGBColor(255,255,255) or RGBColor(0,0,0)
        
        title_line = shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(1.15), Inches(0.8), Inches(0.06))
        title_line.fill.solid()
        title_line.fill.fore_color.rgb = accent
        title_line.line.fill.background()
        
        bullet_box = shapes.add_textbox(Inches(0.7), Inches(1.4), Inches(12), Inches(5.5))
        tf = bullet_box.text_frame
        tf.word_wrap = True
        
        bullets = data.get("bullets", [])
        for i, bullet in enumerate(bullets):
            if i == 0:
                p = tf.paragraphs[0]
            else:
                p = tf.add_paragraph()
            p.text = bullet
            p.font.size = Pt(22)
            p.level = 0
            p.space_before = Pt(14)
            p.font.color.rgb = is_dark and RGBColor(230,230,230) or RGBColor(40,40,40)


def create_from_template(
    slides: List[Dict[str, Any]],
    title: str,
    theme: str = "minimal",
    template_path: Optional[str] = None
) -> Presentation:
    if template_path and os.path.exists(template_path):
        return Presentation(template_path)
    builder = TemplateBuilder(theme)
    return builder.create_presentation(slides, title)


if __name__ == "__main__":
    test = [
        {"title": "Test Slide", "bullets": ["Point 1", "Point 2", "Point 3"]}
    ]
    for t in ["minimal", "modern", "corporate"]:
        b = TemplateBuilder(t)
        b.create_presentation(test, f"Test {t}").save(f"test_{t}.pptx")
    print("Created test files")