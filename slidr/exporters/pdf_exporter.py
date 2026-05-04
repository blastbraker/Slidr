"""PDF exporter for creating PDF files"""

import os
from typing import List, Dict, Any, Optional
from io import BytesIO


class PDFExporter:
    """Export presentation to PDF format"""

    @staticmethod
    def export(
        slides: List[Dict[str, Any]],
        title: str,
        output_path: str,
        theme: str = "minimal",
        template_path: Optional[str] = None
    ):
        """Export slides to PDF file"""
        from slidr.templates.builder import create_from_template

        prs = create_from_template(slides, title, theme, template_path)

        output_pptx = BytesIO()
        prs.save(output_pptx)
        output_pptx.seek(0)

        try:
            from pdf2image import convert_from_bytes
            images = convert_from_bytes(output_pptx.read())

            if images:
                images[0].save(output_path, save_all=True, append_images=images[1:])
        except ImportError:
            prs.save(output_path.replace(".pdf", ".pptx"))
            raise ImportError("pdf2image not installed. Please install: pip install pdf2image[poppler]")
        except Exception as e:
            raise RuntimeError(f"Failed to export PDF: {e}")

        return output_path


def main():
    """Test PDF export"""
    print("PDFExporter loaded - requires pdf2image for PDF conversion")


if __name__ == "__main__":
    main()