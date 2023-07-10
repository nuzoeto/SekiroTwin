import requests

from pyrogram.types import InlineQueryResultPhoto

from megumin import Config

class PexelsImagesAPI:
    def __init__(self):
        self.pexels_results = []
        self.pexels_api_key = Config.PEXELS_API_KEY
        self.pexels_url = "https://api.pexels.com/v1/search"

    def pixabay_image(self, query: str, per_page: int):
        headers = {
            "Authorization": self.pexels_api_key
        }
        params = {
            "query": query,
            "per_page": per_page,
        }
        
        res = requests.get(self.pexels_url, headers=headers, params=params)
        data = res.json()

        images = []
        for image in data["photo"]:
            images.append(image["src"]["large"])
        return images

    def pixabay_results_photo(self, query: str, per_page: int):
        search_results = self.pixabay_image(query, per_page)
        for i, image_url in enumerate(search_results):
            self.pexels_results.append(
                InlineQueryResultPhoto(
                    photo_url=image_url,
                    thumb_url=image_url,
                )
            )
        return self.pexels_results
        
