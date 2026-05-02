"""AI client for Ollama integration"""

import json
import requests
from typing import Optional, List, Dict, Any
from slidr.config import OLLAMA_BASE_URL, OLLAMA_MODEL


class AIClient:
    """Client for interacting with Ollama AI API"""

    def __init__(self, model: str = OLLAMA_MODEL, base_url: str = OLLAMA_BASE_URL):
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.api_endpoint = f"{self.base_url}/api/generate"

    def is_available(self) -> bool:
        """Check if Ollama is running and model is available"""
        try:
            response = requests.get(
                f"{self.base_url}/api/tags",
                timeout=5
            )
            if response.status_code == 200:
                models = response.json().get("models", [])
                model_names = [m.get("name", "").split(":")[0] for m in models]
                return any(self.model.split(":")[0] in name for name in model_names)
            return False
        except requests.exceptions.RequestException:
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
        payload = {
            "model": self.model,
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
            if response.startswith("```json"):
                response = response[7:]
            if response.startswith("```"):
                response = response[3:]
            if response.endswith("```"):
                response = response[:-3]

            slides = json.loads(response.strip())
            if isinstance(slides, list):
                return slides
            return []
        except json.JSONDecodeError:
            return self._fallback_parse(response)

    def _fallback_parse(self, response: str) -> List[Dict[str, Any]]:
        """Fallback parser if JSON parsing fails"""
        slides = []
        lines = response.strip().split("\n")

        current_slide = None
        for line in lines:
            line = line.strip()
            if not line:
                continue

            if line.startswith('"title"') or line.startswith("title"):
                if current_slide:
                    slides.append(current_slide)
                title = line.split(":", 1)[-1].strip().strip('",')
                current_slide = {"title": title, "bullets": [], "notes": ""}
            elif line.startswith('"') and current_slide:
                bullet = line.strip('",').strip('"')
                if bullet and len(bullet) > 2:
                    current_slide["bullets"].append(bullet)

        if current_slide:
            slides.append(current_slide)

        return slides if slides else [{"title": "Overview", "bullets": ["Content generated from topic"], "notes": ""}]


def main():
    """Test the AI client"""
    client = AIClient()
    print(f"Checking Ollama at {client.base_url}...")
    print(f"Model: {client.model}")
    print(f"Available: {client.is_available()}")


if __name__ == "__main__":
    main()