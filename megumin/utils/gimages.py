import requests
from bs4 import BeautifulSoup
import re

from pyrogram.types import InlineQueryResultPhoto

from uuid import uuid4
from google_images_download import GoogleImagesDownload


class GoogleImagesAPI:
    def __init__(self):
        self.results = []
        self.headers = {
            "User-Agent": f"Mozilla/5.0 (Windows NT 10.0;Win64(Build: {uuid4()})) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }

    def resolution(self, url):
        response = requests.get(url)
        code = uuid4()
        with open(f'{code}_image.jpg', 'wb') as f:
            f.write(response.content)
        
        with open(f'{code}_image.jpg', 'rb') as f:
            header = f.read(24)
            try:
                width, height = re.search(rb'(\d+)x(\d+)', header).groups()
                return int(width), int(height)
            except AttributeError:
                return 0, 0
    
    def image(self, query: str, chat_id: str):
        response = GoogleImagesDownload()
        search_params = {"keywords": query, "limit": 10, "print_urls": True, "no_download": True}
        result = response.download(search_params)
        links = result[0][query]
        return links
    
    def results_photo(self, query: str, chat_id: str):
        search_results = self.image(query, chat_id)
        for i, image_url in enumerate(search_results):
            self.results.append(
                InlineQueryResultPhoto(
                    photo_url=image_url,
                    thumb_url=image_url,
                )
            )
        return self.results
            
