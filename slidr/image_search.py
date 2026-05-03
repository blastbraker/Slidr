"""Image search and management for Slidr v2.3"""

import os
import requests
from typing import List, Dict, Optional, Tuple
from urllib.parse import quote


class ImageSearch:
    """Search and manage images for slides"""
    
    # Free image APIs (no key required for basic usage)
    UNSPLASH_SEARCH_URL = "https://api.unsplash.com/search/photos"
    PEXELS_SEARCH_URL = "https://api.pexels.com/v1/search"
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key
    
    def search_unsplash(self, query: str, per_page: int = 10) -> List[Dict]:
        """Search Unsplash for images"""
        if not self.api_key:
            # Try demo/featured images
            return self._get_demo_images(query, per_page)
        
        headers = {
            "Authorization": f"Client-ID {self.api_key}"
        }
        params = {
            "query": query,
            "per_page": per_page,
            "orientation": "landscape"
        }
        
        try:
            resp = requests.get(self.UNSPLASH_SEARCH_URL, headers=headers, params=params, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                return [
                    {
                        "url": photo.get("urls", {}).get("regular"),
                        "thumb": photo.get("urls", {}).get("thumb"),
                        "description": photo.get("description") or photo.get("alt_description", ""),
                        "author": photo.get("user", {}).get("name"),
                        "source": "unsplash"
                    }
                    for photo in data.get("results", [])
                    if photo.get("urls", {}).get("regular")
                ]
        except:
            pass
        
        return self._get_demo_images(query, per_page)
    
    def search_pexels(self, query: str, per_page: int = 10) -> List[Dict]:
        """Search Pexels for images"""
        if not self.api_key:
            return self._get_demo_images(query, per_page)
        
        headers = {"Authorization": self.api_key}
        params = {"query": query, "per_page": per_page}
        
        try:
            resp = requests.get(self.PEXELS_SEARCH_URL, headers=headers, params=params, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                return [
                    {
                        "url": photo.get("src", {}).get("large"),
                        "thumb": photo.get("src", {}).get("medium"),
                        "description": photo.get("alt", ""),
                        "author": photo.get("photographer"),
                        "source": "pexels"
                    }
                    for photo in data.get("photos", [])
                ]
        except:
            pass
        
        return self._get_demo_images(query, per_page)
    
    def _get_demo_images(self, query: str, per_page: int = 10) -> List[Dict]:
        """Return placeholder images when no API key"""
        return [
            {
                "url": None,
                "thumb": None,
                "description": f"Image for: {query}",
                "author": None,
                "source": "placeholder",
                "keywords": query
            }
        ] * min(per_page, 3)
    
    def get_image_from_url(self, url: str) -> Optional[bytes]:
        """Download image from URL"""
        try:
            resp = requests.get(url, timeout=15)
            if resp.status_code == 200:
                return resp.content
        except:
            pass
        return None
    
    def save_image(self, url: str, filepath: str) -> bool:
        """Save image from URL to file"""
        content = self.get_image_from_url(url)
        if content:
            try:
                with open(filepath, "wb") as f:
                    f.write(content)
                return True
            except:
                pass
        return False


def search_images(keywords: str, api_key: str = None) -> List[Dict]:
    """Quick search function"""
    searcher = ImageSearch(api_key)
    results = searcher.search_unsplash(keywords, 6)
    if not results:
        results = searcher.search_pexels(keywords, 6)
    return results


if __name__ == "__main__":
    # Test
    searcher = ImageSearch()
    results = searcher.search_unsplash("technology", 3)
    print(f"Found {len(results)} images")
    for r in results[:2]:
        print(f"  - {r.get('description', 'No description')[:50]}")