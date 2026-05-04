"""Configuration settings for Slidr v3"""

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3.2:3b")

UNSPLASH_ACCESS_KEY = os.environ.get("UNSPLASH_ACCESS_KEY", "")

DEFAULT_SLIDES = 5
MAX_SLIDES = 20
MIN_SLIDES = 3

OUTPUT_FORMATS = ["PPTX", "PDF", "HTML"]

SLIDE_TYPES = {
    "title": {
        "name": "Title Slide",
        "description": "Big title with subtitle",
        "fields": ["title", "subtitle", "image_keywords"],
    },
    "content": {
        "name": "Content",
        "description": "Title, subtitle and bullet points",
        "fields": ["title", "subtitle", "bullets", "image_keywords"],
    },
    "bullets_image": {
        "name": "Bullets + Image",
        "description": "Left bullets, right image",
        "fields": ["title", "bullets", "image_keywords", "image_url"],
    },
    "two_column": {
        "name": "Two Column",
        "description": "Two content columns side by side",
        "fields": ["title", "bullets", "image_keywords"],
    },
    "divider": {
        "name": "Divider",
        "description": "Section transition with centered title",
        "fields": ["title", "subtitle"],
    },
    "quote": {
        "name": "Quote",
        "description": "Big quote with author citation",
        "fields": ["quote", "author", "title", "image_keywords"],
    },
    "statistic": {
        "name": "Statistic",
        "description": "Large number with label and context",
        "fields": ["big_number", "stat_label", "subtitle", "title"],
    },
    "comparison": {
        "name": "Comparison",
        "description": "Pros vs cons or two-column comparison",
        "fields": ["title", "left_title", "left_items", "right_title", "right_items", "image_keywords"],
    },
    "timeline": {
        "name": "Timeline",
        "description": "Chronological events",
        "fields": ["title", "events", "image_keywords"],
    },
    "full_image": {
        "name": "Full Image",
        "description": "Hero image with caption overlay",
        "fields": ["image_url", "caption", "title", "overlay_title"],
    },
}

SLIDE_TYPE_FIELDS = {
    "title": ["title", "subtitle", "image_keywords"],
    "content": ["title", "subtitle", "bullets", "image_keywords"],
    "bullets_image": ["title", "bullets", "image_keywords", "image_url"],
    "two_column": ["title", "bullets", "image_keywords"],
    "divider": ["title", "subtitle"],
    "quote": ["quote", "author", "title", "image_keywords"],
    "statistic": ["big_number", "stat_label", "subtitle", "title"],
    "comparison": ["title", "left_title", "left_items", "right_title", "right_items", "image_keywords"],
    "timeline": ["title", "events", "image_keywords"],
    "full_image": ["image_url", "caption", "title", "overlay_title"],
}

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