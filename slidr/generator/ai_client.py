"""AI client for Ollama integration - v2.1 with rich content"""

import json
import re
import requests
from typing import List, Dict, Any, Optional
from slidr.config import OLLAMA_BASE_URL, OLLAMA_MODEL


# Slide types for v2.1
SLIDE_TYPES = ["title", "content", "bullets_image", "two_column", "divider"]


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
        return f"""Create a professional presentation outline about: {topic}

Generate exactly {num_slides} slides in JSON format. For each slide include:
- type: slide type (title, content, bullets_image, two_column, divider)
- title: The slide title
- subtitle: A brief subtitle (for title slides) or short description
- bullets: List of 3-5 key bullet points
- image_keywords: 2-3 keywords for an image that represents this slide
- speaker_notes: Brief speaker notes

For a {num_slides}-slide presentation:
- 1 title slide (type: title) - Introduction/overview
- {num_slides-2} content slides (mix of content, bullets_image, two_column)
- 1 divider slide (type: divider) - Key section transition

Return ONLY valid JSON array (no code blocks, no explanation):
[
  {{"type": "title", "title": "Main Title", "subtitle": "Subtitle", "bullets": [], "image_keywords": "keywords", "notes": "notes"}},
  {{"type": "content", "title": "Title", "subtitle": "", "bullets": ["Point 1", "Point 2"], "image_keywords": "", "notes": "notes"}},
  ...
]

Return only the JSON array, no other text."""

    def _build_prompt_from_text(self, text: str, num_slides: int = 6) -> str:
        return f"""Based on the following content, create a professional presentation outline.

Content:
{text[:5000]}

Generate exactly {num_slides} slides in JSON format. For each slide include:
- type: slide type (title, content, bullets_image, two_column, divider)
- title: The slide title
- subtitle: A brief subtitle or short description
- bullets: List of 3-5 key bullet points
- image_keywords: 2-3 keywords for an image
- speaker_notes: Brief speaker notes

Return ONLY valid JSON array (no code blocks):
[
  {{"type": "title", "title": "Main Title", "subtitle": "Subtitle", "bullets": [], "image_keywords": "keywords", "notes": "notes"}},
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
            
            # Find JSON array
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
                # Ensure all required fields
                for slide in slides:
                    if "type" not in slide:
                        slide["type"] = "content"
                    if "subtitle" not in slide:
                        slide["subtitle"] = ""
                    if "image_keywords" not in slide:
                        slide["image_keywords"] = ""
                    if "notes" not in slide:
                        slide["notes"] = ""
                    if "bullets" not in slide:
                        slide["bullets"] = []
                return slides
            return []
        except json.JSONDecodeError:
            return self._fallback_parse(response)

    def _fallback_parse(self, response: str) -> List[Dict[str, Any]]:
        """Fallback parser with rich content support"""
        slides = []
        
        # Try to extract using regex
        titles = re.findall(r'"title"\s*:\s*"([^"]+)"', response, re.IGNORECASE)
        types = re.findall(r'"type"\s*:\s*"([^"]+)"', response, re.IGNORECASE)
        subtitles = re.findall(r'"subtitle"\s*:\s*"([^"]+)"', response, re.IGNORECASE)
        bullets_blocks = re.findall(r'"bullets"\s*:\s*\[([^\]]+)\]', response, re.DOTALL)
        keywords = re.findall(r'"image_keywords"\s*:\s*"([^"]+)"', response, re.IGNORECASE)
        notes = re.findall(r'"notes"\s*:\s*"([^"]+)"', response, re.IGNORECASE)
        
        for i, title in enumerate(titles):
            slide_type = types[i] if i < len(types) else "content"
            subtitle = subtitles[i] if i < len(subtitles) else ""
            image_kw = keywords[i] if i < len(keywords) else ""
            note = notes[i] if i < len(notes) else ""
            
            bullets = []
            if i < len(bullets_blocks):
                items = bullets_blocks[i].split(",")
                for item in items:
                    item = item.strip().strip('"\'[],')
                    if item:
                        bullets.append(item)
            
            slides.append({
                "type": slide_type,
                "title": title.strip(),
                "subtitle": subtitle.strip(),
                "bullets": bullets,
                "image_keywords": image_kw.strip(),
                "notes": note.strip()
            })
        
        if not slides:
            # Last resort: simple parse
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