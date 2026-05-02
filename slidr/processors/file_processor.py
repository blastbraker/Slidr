"""File processor for extracting text from PDF and DOCX files"""

import os
from typing import Optional
import fitz
from docx import Document


class FileProcessor:
    """Extract text content from various file formats"""

    @staticmethod
    def extract_text(file_path: str) -> str:
        """Extract text from a file based on its extension"""
        ext = os.path.splitext(file_path)[1].lower()

        if ext == ".pdf":
            return FileProcessor._extract_pdf(file_path)
        elif ext in [".docx", ".doc"]:
            return FileProcessor._extract_docx(file_path)
        elif ext == ".txt":
            return FileProcessor._extract_txt(file_path)
        else:
            raise ValueError(f"Unsupported file format: {ext}")

    @staticmethod
    def _extract_pdf(file_path: str) -> str:
        """Extract text from PDF using PyMuPDF"""
        text_parts = []
        try:
            doc = fitz.open(file_path)
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                text_parts.append(page.get_text())
            doc.close()
        except Exception as e:
            raise RuntimeError(f"Failed to extract PDF: {e}")

        return "\n\n".join(text_parts)

    @staticmethod
    def _extract_docx(file_path: str) -> str:
        """Extract text from DOCX using python-docx"""
        try:
            doc = Document(file_path)
            paragraphs = [para.text for para in doc.paragraphs if para.text.strip()]
            return "\n\n".join(paragraphs)
        except Exception as e:
            raise RuntimeError(f"Failed to extract DOCX: {e}")

    @staticmethod
    def _extract_txt(file_path: str) -> str:
        """Extract text from TXT file"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            raise RuntimeError(f"Failed to extract TXT: {e}")

    @staticmethod
    def is_supported(file_path: str) -> bool:
        """Check if file format is supported"""
        ext = os.path.splitext(file_path)[1].lower()
        return ext in [".pdf", ".docx", ".doc", ".txt"]


def main():
    """Test the file processor"""
    print("FileProcessor loaded successfully")
    print("Supported formats: PDF, DOCX, DOC, TXT")


if __name__ == "__main__":
    main()