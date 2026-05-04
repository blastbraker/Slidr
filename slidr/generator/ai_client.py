"""AI client for Ollama integration - v3 with auto-layout selection"""

import json
import re
import requests
from typing import List, Dict, Any, Optional
from slidr.config import OLLAMA_BASE_URL, OLLAMA_MODEL


SLIDE_TYPES = [
    "title", "content", "bullets_image", "two_column", "divider",
    "quote", "statistic", "comparison", "timeline", "full_image"
]


class AIClient:
    """Client for interacting with Ollama AI API"""

    def __init__(self, model: str = "llama3.2:3b", base_url: str = OLLAMA_BASE_URL):
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.api_endpoint = f"{self.base_url}/api/generate"

    def is_available(self) -> bool:
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200 and len(response.json().get("models", [])) > 0
        except:
            return False

    def generate_slides(self, topic: str, num_slides: int = 6) -> List[Dict[str, Any]]:
        """Generate rich slide content from a topic"""
        prompt = self._build_prompt(topic, num_slides)
        response = self._generate(prompt)
        return self._parse_slides(response)

    def generate_from_text(self, text: str, num_slides: int = 6) -> List[Dict[str, Any]]:
        """Generate rich slide content from extracted text"""
        prompt = self._build_prompt_from_text(text, num_slides)
        response = self._generate(prompt)
        return self._parse_slides(response)

    def _build_prompt(self, topic: str, num_slides: int = 6) -> str:
        return f"""Create a professional presentation about: {topic}

Generate exactly {num_slides} slides in JSON format. Choose the BEST slide type for each content:

Available slide types:
- title: Main presentation title slide (big title + subtitle)
- content: Standard content (title + subtitle + bullets)
- bullets_image: Content with image on right side
- two_column: Two columns of content
- divider: Section transition (big centered title)
- quote: Quote or testimonial with author
- statistic: Big number with label (e.g., "85%", "$1B", "3x")
- comparison: Two-column comparison (pros/cons, before/after)
- timeline: Chronological events with dates
- full_image: Full-bleed image with caption overlay

AI should auto-select the best layout based on content. For example:
- First slide = title
- Data/metrics slides = statistic  
- Comparisons = comparison
- History/timeline = timeline
- Quotes from sources = quote
- Image-heavy slides = bullets_image or full_image
- Section breaks = divider

For each slide, include appropriate fields:
- type: auto-selected layout
- title: The slide title
- subtitle: Brief description (use for content, statistic)
- bullets: 2-5 key points (use for content, bullets_image, two_column)
- image_keywords: Keywords for relevant image
- quote: The quote text (for quote layout)
- author: Quote author (for quote layout)
- big_number: Large number like "85%" or "$1B" (for statistic)
- stat_label: Label for the number (for statistic)  
- left_title: Title for left column (for comparison)
- left_items: Items for left column (for comparison)
- right_title: Title for right column (for comparison)
- right_items: Items for right column (for comparison)
- events: Array of {{"date": "2020", "title": "Event"}} (for timeline)
- image_url: Direct image URL (for full_image, bullets_image)
- caption: Image caption (for full_image)
- notes: Speaker notes

For a {num_slides}-slide presentation, ensure variety.

Return ONLY valid JSON array (no code blocks, no explanation):
[
  {{"type": "title", "title": "Main Title", "subtitle": "Subtitle", "bullets": [], "image_keywords": "keywords", "notes": ""}},
  {{"type": "statistic", "title": "", "subtitle": "", "big_number": "85%", "stat_label": "Growth", "image_keywords": ""}},
  {{"type": "comparison", "title": "Analysis", "left_title": "Pros", "left_items": ["Point 1", "Point 2"], "right_title": "Cons", "right_items": ["Point 1", "Point 2"], "image_keywords": ""}},
  {{"type": "timeline", "title": "History", "events": [{{"date": "2020", "title": "Event 1"}}, {{"date": "2021", "title": "Event 2"}}], "image_keywords": ""}},
  {{"type": "quote", "quote": "Famous quote", "author": "Author Name", "title": "", "image_keywords": ""}},
  ...
]

Return only the JSON array, no other text."""

    def _build_prompt_from_text(self, text: str, num_slides: int = 6) -> str:
        return f"""Based on the following content, create a professional presentation outline.

Content:
{text[:5000]}

Generate exactly {num_slides} slides in JSON format. Choose the BEST slide type for each content:

Available slide types:
- title, content, bullets_image, two_column, divider
- quote, statistic, comparison, timeline, full_image

AI should auto-select the best layout based on content.

For each slide, include appropriate fields (type, title, subtitle, bullets, image_keywords, etc.)
For statistic: big_number, stat_label
For comparison: left_title, left_items, right_title, right_items  
For timeline: events array
For quote: quote, author
For full_image: image_url, caption

Return ONLY valid JSON array (no code blocks):
[
  {{"type": "title", "title": "Main Title", "subtitle": "Subtitle", "bullets": [], "image_keywords": "keywords", "notes": ""}},
  ...
]

Return only the JSON array, no other text."""

    def _generate(self, prompt: str, max_tokens: int = 2048) -> str:
        model_to_use = getattr(self, 'available_model', self.model)
        
        payload = {
            "model": model_to_use,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "num_predict": max_tokens,
            }
        }

        try:
            response = requests.post(self.api_endpoint, json=payload, timeout=120)
            response.raise_for_status()
            return response.json().get("response", "")
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Failed to connect to Ollama: {e}")

    def _parse_slides(self, response: str) -> List[Dict[str, Any]]:
        """Parse AI response into slide structure with rich content"""
        try:
            response = response.strip()
            
            start = response.find("[")
            end = response.rfind("]")
            
            if start >= 0 and end > start:
                response = response[start:end+1]
            elif "```json" in response:
                response = response.split("```json")[1].split("```")[0]
            elif "```" in response:
                response = response.split("```")[1].split("```")[0]
            
            slides = json.loads(response.strip())
            
            if isinstance(slides, list):
                for slide in slides:
                    slide = self._normalize_slide(slide)
                return slides
            return []
        except json.JSONDecodeError:
            return self._fallback_parse(response)

    def _normalize_slide(self, slide: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize slide with all required fields"""
        slide_type = slide.get("type", "content")
        
        base_fields = {
            "type": slide_type,
            "title": slide.get("title", ""),
            "subtitle": slide.get("subtitle", ""),
            "bullets": slide.get("bullets", []),
            "image_keywords": slide.get("image_keywords", ""),
            "image_url": slide.get("image_url", ""),
            "notes": slide.get("notes", ""),
        }
        
        if slide_type == "quote":
            base_fields.update({
                "quote": slide.get("quote", ""),
                "author": slide.get("author", ""),
            })
        elif slide_type == "statistic":
            base_fields.update({
                "big_number": slide.get("big_number", ""),
                "stat_label": slide.get("stat_label", ""),
            })
        elif slide_type == "comparison":
            base_fields.update({
                "left_title": slide.get("left_title", ""),
                "left_items": slide.get("left_items", slide.get("bullets", [])[:3]),
                "right_title": slide.get("right_title", ""),
                "right_items": slide.get("right_items", slide.get("bullets", [])[3:] if len(slide.get("bullets", [])) > 3 else []),
            })
        elif slide_type == "timeline":
            base_fields.update({
                "events": slide.get("events", []),
            })
        elif slide_type == "full_image":
            base_fields.update({
                "caption": slide.get("caption", ""),
                "overlay_title": slide.get("overlay_title", ""),
            })
        
        base_fields.setdefault("author", "")
        base_fields.setdefault("quote", "")
        base_fields.setdefault("big_number", "")
        base_fields.setdefault("stat_label", "")
        base_fields.setdefault("left_title", "")
        base_fields.setdefault("left_items", [])
        base_fields.setdefault("right_title", "")
        base_fields.setdefault("right_items", [])
        base_fields.setdefault("events", [])
        base_fields.setdefault("caption", "")
        base_fields.setdefault("overlay_title", "")
        
        return base_fields

    def _fallback_parse(self, response: str) -> List[Dict[str, Any]]:
        """Fallback parser with rich content support"""
        slides = []
        
        titles = re.findall(r'"title"\s*:\s*"([^"]+)"', response, re.IGNORECASE)
        types = re.findall(r'"type"\s*:\s*"([^"]+)"', response, re.IGNORECASE)
        subtitles = re.findall(r'"subtitle"\s*:\s*"([^"]+)"', response, re.IGNORECASE)
        bullets_blocks = re.findall(r'"bullets"\s*:\s*\[([^\]]+)\]', response, re.DOTALL)
        keywords = re.findall(r'"image_keywords"\s*:\s*"([^"]+)"', response, re.IGNORECASE)
        quotes = re.findall(r'"quote"\s*:\s*"([^"]+)"', response, re.IGNORECASE)
        authors = re.findall(r'"author"\s*:\s*"([^"]+)"', response, re.IGNORECASE)
        big_numbers = re.findall(r'"big_number"\s*:\s*"([^"]+)"', response, re.IGNORECASE)
        stat_labels = re.findall(r'"stat_label"\s*:\s*"([^"]+)"', response, re.IGNORECASE)
        
        for i, title in enumerate(titles):
            slide_type = types[i] if i < len(types) else "content"
            subtitle = subtitles[i] if i < len(subtitles) else ""
            image_kw = keywords[i] if i < len(keywords) else ""
            
            bullets = []
            if i < len(bullets_blocks):
                items = bullets_blocks[i].split(",")
                for item in items:
                    item = item.strip().strip('"\'[],')
                    if item:
                        bullets.append(item)
            
            slide = {
                "type": slide_type,
                "title": title.strip(),
                "subtitle": subtitle.strip(),
                "bullets": bullets,
                "image_keywords": image_kw.strip(),
                "notes": "",
            }
            
            if slide_type == "quote" and i < len(quotes):
                slide["quote"] = quotes[i].strip()
                slide["author"] = authors[i].strip() if i < len(authors) else ""
            
            if slide_type == "statistic" and i < len(big_numbers):
                slide["big_number"] = big_numbers[i].strip()
                slide["stat_label"] = stat_labels[i].strip() if i < len(stat_labels) else ""
            
            slides.append(slide)
        
        if not slides:
            lines = response.replace("{", "").replace("}", "").split("\n")
            current = {"type": "content", "title": "", "subtitle": "", "bullets": [], "image_keywords": "", "notes": ""}
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                if len(line) < 60 and not line.startswith(("•", "-", "*")):
                    if current["title"]:
                        slides.append(current)
                    current = {"type": "content", "title": line, "subtitle": "", "bullets": [], "image_keywords": "", "notes": ""}
                elif line.startswith(("-", "*", "•")):
                    current["bullets"].append(line.lstrip("-*• ").strip())
            
            if current["title"]:
                slides.append(current)
        
        return slides if slides else [{"type": "content", "title": "Overview", "subtitle": "", "bullets": ["Content generated from topic"], "image_keywords": "", "notes": ""}]