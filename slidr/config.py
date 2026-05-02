"""Configuration settings for Slidr"""

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3.2:3b")

DEFAULT_SLIDES = 5
MAX_SLIDES = 20
MIN_SLIDES = 3

OUTPUT_FORMATS = ["PPTX", "PDF", "HTML"]

TEMPLATES = {
    "minimal": {
        "name": "Minimal",
        "description": "Clean modern look with accent colors",
        "primary_color": "F5F5F5",
        "accent_color": "2D5A8C",
        "text_color": "1A1A1A",
        "font_name": "Arial",
    },
    "modern": {
        "name": "Modern",
        "description": "Dark theme with accent bar",
        "primary_color": "1E1E1E",
        "accent_color": "4A90D9",
        "text_color": "FFFFFF",
        "font_name": "Segoe UI",
    },
    "corporate": {
        "name": "Corporate",
        "description": "Professional blue/gray",
        "primary_color": "2C3E50",
        "accent_color": "3498DB",
        "text_color": "FFFFFF",
        "font_name": "Calibri",
    },
}