import requests
from bs4 import BeautifulSoup
import re

from pyrogram.types import InlineQueryResultPhoto

from uuid import uuid4

class GoogleImagesApi:
    def __init__(self, query):
        self.query = query
        self.results = []
        self.headers = {
            f"User-Agent": "Mozilla/5.0 (Windows NT 10.0;Win64(Build: {uuid4()})) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
    
    def image(self, chat_id: str):
        url = "https://www.google.com/search?tbm=isch&q=" + self.query
        response = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        images = []
        for img in soup.find_all('img'):
            src = img['src']
            if src.startswith('http') and re.match(r'^https?://\S+$', src):
                images.append(src)
        
        return images[:10]
    
    def results_photo(self):
        search_results = self.image(chat_id)
        for i, image_url in enumerate(search_results):
            self.results.append(
                InlineQueryResultPhoto(
                    photo_url=image_url,
                    thumb_url=image_url,
                )
            )
        return results
            
