"""Template builder v2.1 - Multiple slide layouts"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from typing import List, Dict, Any, Optional
import os


SLIDE_TYPES = {
    "title": "Title Slide - Big title with subtitle",
    "content": "Content - Title and bullet points",
    "bullets_image": "Bullets + Image - Title, bullets on left, image placeholder on right",
    "two_column": "Two Column - Two content areas side by side",
    "divider": "Divider - Big centered title for section transitions"
}

class TemplateBuilder:
    """Professional templates with multiple layouts"""

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

        for i, slide_data in enumerate(slides):
            slide_type = slide_data.get("type", "content")
            content_slide = prs.slides.add_slide(prs.slide_layouts[6])
            
            if slide_type == "title":
                self._layout_title(content_slide, slide_data)
            elif slide_type == "divider":
                self._layout_divider(content_slide, slide_data)
            elif slide_type == "bullets_image":
                self._layout_bullets_image(content_slide, slide_data)
            elif slide_type == "two_column":
                self._layout_two_column(content_slide, slide_data)
            else:
                self._layout_content(content_slide, slide_data)

        return prs

    def _add_background(self, shapes, primary_color: str = None):
        c = self.colors
        bg = shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = self._rgb(primary_color or c["primary"])
        bg.line.fill.background()
        return bg

    def _layout_title(self, slide, data: Dict[str, Any]):
        c = self.colors
        s = slide.shapes
        self._add_background(s)
        
        # Accent bar
        bar = s.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(0.1), Inches(7.5))
        bar.fill.solid()
        bar.fill.fore_color.rgb = self._rgb(c["accent"])
        bar.line.fill.background()
        
        # Title
        tb = s.add_textbox(Inches(1.5), Inches(2.2), Inches(10), Inches(2))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = data.get("title", "Presentation")
        p.font.size = Pt(52)
        p.font.bold = True
        p.font.color.rgb = RGBColor(255, 255, 255)
        
        # Subtitle
        sub = data.get("subtitle", "")
        if sub:
            sb = s.add_textbox(Inches(1.5), Inches(4.2), Inches(8), Inches(0.8))
            tf = sb.text_frame
            p = tf.paragraphs[0]
            p.text = sub
            p.font.size = Pt(24)
            p.font.color.rgb = self._rgb(c["accent"])

    def _layout_content(self, slide, data: Dict[str, Any]):
        c = self.colors
        s = slide.shapes
        self._add_background(s)
        
        # Header
        hdr = s.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.9))
        hdr.fill.solid()
        hdr.fill.fore_color.rgb = self._rgb(c["accent"])
        hdr.line.fill.background()
        
        # Title
        tb = s.add_textbox(Inches(0.5), Inches(0.2), Inches(12), Inches(0.7))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = data.get("title", "Slide")
        p.font.size = Pt(28)
        p.font.bold = True
        p.font.color.rgb = RGBColor(255, 255, 255)
        
        # Subtitle
        sub = data.get("subtitle", "")
        if sub:
            sb = s.add_textbox(Inches(0.5), Inches(1.0), Inches(12), Inches(0.5))
            tf = sb.text_frame
            p = tf.paragraphs[0]
            p.text = sub
            p.font.size = Pt(14)
            p.font.color.rgb = RGBColor(200, 200, 200)
        
        # Bullets
        y = 1.5 if sub else 1.2
        bb = s.add_textbox(Inches(0.5), Inches(y), Inches(12), Inches(5))
        tf = bb.text_frame
        tf.word_wrap = True
        
        for i, b in enumerate(data.get("bullets", [])):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.text = b
            p.font.size = Pt(20)
            p.level = 0
            p.space_before = Pt(12)
            p.font.color.rgb = RGBColor(230, 230, 230)

    def _layout_bullets_image(self, slide, data: Dict[str, Any]):
        c = self.colors
        s = slide.shapes
        self._add_background(s)
        
        # Header
        hdr = s.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.9))
        hdr.fill.solid()
        hdr.fill.fore_color.rgb = self._rgb(c["accent"])
        hdr.line.fill.background()
        
        # Title
        tb = s.add_textbox(Inches(0.5), Inches(0.2), Inches(6), Inches(0.7))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = data.get("title", "Slide")
        p.font.size = Pt(28)
        p.font.bold = True
        p.font.color.rgb = RGBColor(255, 255, 255)
        
        # Left: Bullets
        bb = s.add_textbox(Inches(0.5), Inches(1.1), Inches(5.5), Inches(5))
        tf = bb.text_frame
        tf.word_wrap = True
        
        for i, b in enumerate(data.get("bullets", [])):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.text = b
            p.font.size = Pt(18)
            p.level = 0
            p.space_before = Pt(10)
            p.font.color.rgb = RGBColor(230, 230, 230)
        
        # Right: Image area
        kw = data.get("image_keywords", "")
        image_url = data.get("image_url", "")
        
        if image_url and image_url.startswith("http"):
            # Just show placeholder text - image URL is saved for reference
            img_text = f"[Image: {kw}]"
        elif kw:
            img_text = f"[Image: {kw}]"
        else:
            img_text = "[Image placeholder]"
        
        if image_url and image_url.startswith("http"):
            # Just show placeholder text - image URL is saved for reference
            img_text = f"[Image: {kw}]"
        elif kw:
            img_text = f"[Image: {kw}]"
        else:
            img_text = "[Image placeholder]"
        
        # Show placeholder box
        img_box = s.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.2), Inches(1.1), Inches(6.5), Inches(5.2))
        img_box.fill.solid()
        img_box.fill.fore_color.rgb = RGBColor(60, 60, 60)
        img_box.line.color.rgb = self._rgb(c["accent"])
        
        tb = s.add_textbox(Inches(6.2), Inches(3.5), Inches(6.5), Inches(1))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = img_text
        
        p.font.size = Pt(16)
        p.alignment = PP_ALIGN.CENTER
        p.font.color.rgb = RGBColor(150, 150, 150)

    def _layout_two_column(self, slide, data: Dict[str, Any]):
        c = self.colors
        s = slide.shapes
        self._add_background(s)
        
        # Header
        hdr = s.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.9))
        hdr.fill.solid()
        hdr.fill.fore_color.rgb = self._rgb(c["accent"])
        hdr.line.fill.background()
        
        # Title
        tb = s.add_textbox(Inches(0.5), Inches(0.2), Inches(12), Inches(0.7))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = data.get("title", "Slide")
        p.font.size = Pt(28)
        p.font.bold = True
        p.font.color.rgb = RGBColor(255, 255, 255)
        
        # Left column
        left = s.add_textbox(Inches(0.5), Inches(1.1), Inches(5.8), Inches(5))
        tf = left.text_frame
        tf.word_wrap = True
        
        bullets = data.get("bullets", [])
        left_bullets = bullets[:3] if bullets else ["Point 1", "Point 2"]
        
        for i, b in enumerate(left_bullets):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.text = b
            p.font.size = Pt(18)
            p.level = 0
            p.space_before = Pt(10)
            p.font.color.rgb = RGBColor(230, 230, 230)
        
        # Divider line
        div = s.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.5), Inches(1.1), Inches(0.03), Inches(5))
        div.fill.solid()
        div.fill.fore_color.rgb = self._rgb(c["accent"])
        div.line.fill.background()
        
        # Right column
        right = s.add_textbox(Inches(7), Inches(1.1), Inches(5.8), Inches(5))
        tf = right.text_frame
        tf.word_wrap = True
        
        right_bullets = bullets[3:] if len(bullets) > 3 else ["Point 4", "Point 5"]
        
        for i, b in enumerate(right_bullets):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.text = b
            p.font.size = Pt(18)
            p.level = 0
            p.space_before = Pt(10)
            p.font.color.rgb = RGBColor(230, 230, 230)

    def _layout_divider(self, slide, data: Dict[str, Any]):
        c = self.colors
        s = slide.shapes
        self._add_background(s, c["accent"])
        
        # Title
        tb = s.add_textbox(Inches(1), Inches(2.8), Inches(11.333), Inches(2.5))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = data.get("title", "Section")
        p.font.size = Pt(56)
        p.font.bold = True
        p.alignment = PP_ALIGN.CENTER
        p.font.color.rgb = RGBColor(255, 255, 255)
        
        # Subtitle
        sub = data.get("subtitle", "")
        if sub:
            sb = s.add_textbox(Inches(1), Inches(5), Inches(11.333), Inches(1))
            tf = sb.text_frame
            p = tf.paragraphs[0]
            p.text = sub
            p.font.size = Pt(24)
            p.alignment = PP_ALIGN.CENTER
            p.font.color.rgb = RGBColor(255, 255, 255)


def create_from_template(slides: List[Dict[str, Any]], title: str, theme: str = "minimal", template_path: Optional[str] = None) -> Presentation:
    if template_path and os.path.exists(template_path):
        return Presentation(template_path)
    return TemplateBuilder(theme).create_presentation(slides, title)


if __name__ == "__main__":
    test = [
        {"type": "title", "title": "Introduction to AI", "subtitle": "Exploring the Future", "bullets": [], "image_keywords": "artificial intelligence", "notes": ""},
        {"type": "content", "title": "What is AI?", "subtitle": "Understanding artificial intelligence", "bullets": ["Machine learning", "Neural networks", "Deep learning"], "image_keywords": "", "notes": ""},
        {"type": "bullets_image", "title": "Applications", "subtitle": "", "bullets": ["Healthcare", "Finance", "Transportation"], "image_keywords": "technology", "notes": ""},
        {"type": "two_column", "title": "Benefits & Challenges", "subtitle": "", "bullets": ["Efficiency", "Ethics", "Jobs", "Privacy"], "image_keywords": "", "notes": ""},
        {"type": "divider", "title": "Conclusion", "subtitle": "", "bullets": [], "image_keywords": "", "notes": ""},
    ]
    for t in ["minimal", "modern", "corporate"]:
        TemplateBuilder(t).create_presentation(test, f"Test {t}").save(f"test_{t}.pptx")
    print("Created test files")