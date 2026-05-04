"""Image search and management for Slidr"""

import os
import requests
from typing import List, Dict, Optional
from slidr.config import UNSPLASH_ACCESS_KEY


class ImageSearch:
    """Search and manage images for slides"""
    
    UNSPLASH_SEARCH_URL = "https://api.unsplash.com/search/photos"
    PEXELS_SEARCH_URL = "https://api.pexels.com/v1/search"
    
    def __init__(self):
        self.api_key = UNSPLASH_ACCESS_KEY
    
    def search_unsplash(self, query: str, per_page: int = 10) -> List[Dict]:
        """Search Unsplash for images"""
        if not self.api_key:
            return self._get_demo_images(query, per_page)
        
        headers = {"Authorization": f"Client-ID {self.api_key}"}
        params = {"query": query, "per_page": per_page, "orientation": "landscape"}
        
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
            elif resp.status_code == 401:
                print("Invalid Unsplash API key")
        except Exception as e:
            print(f"Unsplash search error: {e}")
        
        return self._get_demo_images(query, per_page)
    
    def _get_demo_images(self, query: str, per_page: int = 10) -> List[Dict]:
        """Return placeholder images when no API key"""
        return [
            {
                "url": None,
                "thumb": None,
                "description": f"Image for: {query}",
                "author": None,
                "source": "placeholder"
            }
        ] * min(per_page, 3)
    
    def search_images(self, keywords: str) -> List[Dict]:
        """Quick search function"""
        results = self.search_unsplash(keywords, 6)
        return results


if __name__ == "__main__":
    # Test
    searcher = ImageSearch()
    results = searcher.search_unsplash("technology", 3)
    print(f"Found {len(results)} images")
    for r in results[:2]:
        print(f"  - {r.get('description', 'No description')[:50]}")