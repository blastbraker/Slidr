"""AI client for Ollama integration"""

import json
import requests
from typing import Optional, List, Dict, Any
from slidr.config import OLLAMA_BASE_URL, OLLAMA_MODEL


class AIClient:
    """Client for interacting with Ollama AI API"""

    def __init__(self, model: str = "llama3.2:3b", base_url: str = OLLAMA_BASE_URL):
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.api_endpoint = f"{self.base_url}/api/generate"
        self.available_model = self._find_text_model()

    def _find_text_model(self) -> str:
        """Find a text-only model"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get("models", [])
                for m in models:
                    name = m.get("name", "")
                    if name and "vision" not in name.lower():
                        return name.split(":")[0] + ":3b"
                if models:
                    return models[0].get("name", "llama3.2:3b")
            return "llama3.2:3b"
        except:
            return "llama3.2:3b"

    def is_available(self) -> bool:
        """Check if Ollama is running and a model is available"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200 and len(response.json().get("models", [])) > 0
        except:
            return False

    def generate_slides(self, topic: str, num_slides: int = 5) -> List[Dict[str, Any]]:
        """Generate slide content from a topic"""
        prompt = f"""Create a presentation outline about: {topic}

Generate exactly {num_slides} slides in JSON format. For each slide include:
- title: The slide title
- bullets: List of 3-5 key bullet points
- speaker_notes: Brief speaker notes

Return ONLY valid JSON in this format:
[
  {{"title": "Slide Title", "bullets": ["Point 1", "Point 2", "Point 3"], "notes": "Speaker notes"}},
  ...
]

Return only the JSON, no other text."""

        response = self._generate(prompt)
        return self._parse_slides(response)

    def generate_from_text(self, text: str, num_slides: int = 5) -> List[Dict[str, Any]]:
        """Generate slide content from extracted text"""
        prompt = f"""Based on the following content, create a presentation outline.

Content:
{text[:5000]}

Generate exactly {num_slides} slides in JSON format. For each slide include:
- title: The slide title
- bullets: List of 3-5 key bullet points
- speaker_notes: Brief speaker notes

Return ONLY valid JSON in this format:
[
  {{"title": "Slide Title", "bullets": ["Point 1", "Point 2", "Point 3"], "notes": "Speaker notes"}},
  ...
]

Return only the JSON, no other text."""

        response = self._generate(prompt)
        return self._parse_slides(response)

    def _generate(self, prompt: str, max_tokens: int = 2048) -> str:
        """Generate text using Ollama API"""
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
            response = requests.post(
                self.api_endpoint,
                json=payload,
                timeout=120
            )
            response.raise_for_status()
            return response.json().get("response", "")
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Failed to connect to Ollama: {e}")

    def _parse_slides(self, response: str) -> List[Dict[str, Any]]:
        """Parse AI response into slide structure"""
        try:
            response = response.strip()
            
            # Find JSON array in response
            start_idx = response.find("[")
            end_idx = response.rfind("]")
            
            if start_idx >= 0 and end_idx > start_idx:
                response = response[start_idx:end_idx+1]
            elif start_idx < 0:
                # Try to extract from code blocks
                if "```json" in response:
                    response = response.split("```json")[1].split("```")[0]
                elif "```" in response:
                    response = response.split("```")[1].split("```")[0]
                else:
                    return self._fallback_parse(response)
            
            response = response.strip()
            slides = json.loads(response)
            if isinstance(slides, list):
                return slides
            return []
        except json.JSONDecodeError:
            return self._fallback_parse(response)

    def _fallback_parse(self, response: str) -> List[Dict[str, Any]]:
        """Fallback parser - extract title/bullets pattern"""
        slides = []
        
        # Look for patterns like "title": or just titles
        import re
        
        # Find all slide sections
        slide_patterns = re.findall(r'["\']?title["\']?\s*:\s*["\']?([^"\']+)["\']?', response, re.IGNORECASE)
        bullet_patterns = re.findall(r'["\']?bullets["\']?\s*:\s*\[([^\]]+)\]', response, re.DOTALL)
        
        if slide_patterns:
            for i, title in enumerate(slide_patterns):
                bullets = []
                if i < len(bullet_patterns):
                    # Extract bullet items
                    items = bullet_patterns[i].split(",")
                    for item in items:
                        item = item.strip().strip('"\'[],')
                        if item:
                            bullets.append(item)
                
                slides.append({
                    "title": title.strip(),
                    "bullets": bullets if bullets else ["Point content"],
                    "notes": ""
                })
        
        if not slides:
            # Last resort: split by looking for numbered sections
            lines = response.replace("{", "").replace("}", "").split("\n")
            current = {"title": "", "bullets": [], "notes": ""}
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                # Detect title line (shorter, no punctuation)
                if len(line) < 50 and not line.endswith((".", ",", ":")):
                    if current["title"]:
                        slides.append(current)
                    current = {"title": line, "bullets": [], "notes": ""}
                elif line.startswith("-") or line.startswith("*"):
                    current["bullets"].append(line.lstrip("-* ").strip())
            
            if current["title"]:
                slides.append(current)
        
        return slides if slides else [{"title": "Overview", "bullets": ["Content generated from topic"], "notes": ""}]


def main():
    """Test the AI client"""
    client = AIClient()
    print(f"Checking Ollama at {client.base_url}...")
    print(f"Model: {client.model}")
    print(f"Available: {client.is_available()}")


if __name__ == "__main__":
    main()