"""PPTX exporter for creating PowerPoint files"""

from pptx import Presentation
from typing import List, Dict, Any, Optional
import os


class PPTXExporter:
    """Export presentation to PPTX format"""

    @staticmethod
    def export(
        slides: List[Dict[str, Any]],
        title: str,
        output_path: str,
        theme: str = "minimal",
        template_path: Optional[str] = None
    ):
        """Export slides to PPTX file"""
        from slidr.templates.builder import create_from_template

        prs = create_from_template(slides, title, theme, template_path)
        prs.save(output_path)
        return output_path

    @staticmethod
    def save(prs: Presentation, output_path: str):
        """Save presentation to file"""
        prs.save(output_path)


def main():
    """Test PPTX export"""
    test_slides = [
        {"title": "Introduction", "bullets": ["Welcome to Slidr", "AI-powered presentations"], "notes": ""},
        {"title": "How It Works", "bullets": ["Enter topic or upload file", "AI generates content", "Export to multiple formats"], "notes": ""},
        {"title": "Conclusion", "bullets": ["Get started today", "Free and open source"], "notes": ""},
    ]
    print("PPTXExporter loaded - use via GUI or API")


if __name__ == "__main__":
    main()