"""Template builder - Professional colorful templates"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from typing import List, Dict, Any, Optional
import os


class TemplateBuilder:
    """Professional templates with colors"""

    THEMES = {
        "minimal": {"primary": "1E3A5F", "accent": "E74C3C"},
        "modern": {"primary": "1A1A2E", "accent": "E94560"},
        "corporate": {"primary": "2C3E50", "accent": "27AE60"},
    }

    def __init__(self, theme: str = "minimal"):
        self.theme = theme
        self.colors = self.THEMES.get(theme, self.THEMES["minimal"])

    def _rgb(self, h: str) -> RGBColor:
        h = h.lstrip("#")
        return RGBColor(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))

    def create_presentation(self, slides: List[Dict[str, Any]], title: str) -> Presentation:
        prs = Presentation()
        prs.slide_width = Inches(13.333)
        prs.slide_height = Inches(7.5)

        self._title_slide(prs.slides.add_slide(prs.slide_layouts[6]), title)
        for i, sd in enumerate(slides):
            self._content_slide(prs.slides.add_slide(prs.slide_layouts[6]), sd, i)
        return prs

    def _title_slide(self, slide, title: str):
        c = self.colors
        s = slide.shapes
        
        bg = s.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = self._rgb(c["primary"])
        bg.line.fill.background()
        
        bar = s.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(0.1), Inches(7.5))
        bar.fill.solid()
        bar.fill.fore_color.rgb = self._rgb(c["accent"])
        bar.line.fill.background()
        
        tb = s.add_textbox(Inches(1.5), Inches(2.5), Inches(10), Inches(2.5))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(50)
        p.font.bold = True
        p.font.color.rgb = RGBColor(255, 255, 255)

    def _content_slide(self, slide, data: Dict[str, Any], idx: int):
        c = self.colors
        s = slide.shapes
        
        bg = s.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = self._rgb(c["primary"])
        bg.line.fill.background()
        
        hdr = s.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.9))
        hdr.fill.solid()
        hdr.fill.fore_color.rgb = self._rgb(c["accent"])
        hdr.line.fill.background()
        
        tb = s.add_textbox(Inches(0.5), Inches(0.2), Inches(12), Inches(0.7))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = data.get("title", f"Slide {idx + 1}")
        p.font.size = Pt(28)
        p.font.bold = True
        p.font.color.rgb = RGBColor(255, 255, 255)
        
        bb = s.add_textbox(Inches(0.6), Inches(1.2), Inches(12), Inches(5.5))
        tf = bb.text_frame
        tf.word_wrap = True
        
        for i, b in enumerate(data.get("bullets", [])):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.text = b
            p.font.size = Pt(20)
            p.level = 0
            p.space_before = Pt(14)
            p.font.color.rgb = RGBColor(230, 230, 230)


def create_from_template(slides: List[Dict[str, Any]], title: str, theme: str = "minimal", template_path: Optional[str] = None) -> Presentation:
    if template_path and os.path.exists(template_path):
        return Presentation(template_path)
    return TemplateBuilder(theme).create_presentation(slides, title)