import requests

from pyrogram.types import InlineQueryResultPhoto

from megumin import Config

class PixabayImagesAPI:
    def __init__(self):
        self.pixabay_results = []
        self.pixabay_api_key = Config.PIXABAY_API_KEY
        self.pixabay_url = "https://pixabay.com/api/"

    def pixabay_image(self, query: str, per_page: int):
        params = {
            "key": self.pixabay_api_key,
            "q": query,
            "per_page": per_page,
        }
        
        res = requests.get(self.pixabay_url, params=params)
        data = res.json()

        images = []
        for image in data["hits"]:
            images.append(image["largeImageURL"])
        return images

    def pixabay_results_photo(self, query: str, per_page: int):
        search_results = self.pixabay_image(query, per_page)
        for i, image_url in enumerate(search_results):
            self.pixabay_results.append(
                InlineQueryResultPhoto(
                    photo_url=image_url,
                    thumb_url=image_url,
                    thumb_width=200,
                    thumb_height=200,
                )
            )
        return self.pixabay_results
        
