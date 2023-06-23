import requests
from bs4 import BeautifulSoup
import json

def search(query):
    url = f"https://www.gsmarena.com/results.php3?sQuickSearch=yes&sName={query}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    results = []
    for li in soup.select(".makers ul li"):
        name = li.a.text.strip()
        image = li.img["src"]
        link = li.a["href"]
        id = link.split("-")[0].split("_")[-1]
        result = {
            "name": name,
            "image": image,
            "link": link,
            "id": id
        }
        results.append(result)

    return results

def device_info(link):
    url = f"https://www.gsmarena.com/{link}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    specs_list = soup.find("div", class_="specs-list")
    if specs_list:
        processor = specs_list.find("td", text="CPU").find_next("td").text.strip()
        battery = specs_list.find("td", text="Battery").find_next("td").text.strip()
        ram = specs_list.find("td", text="RAM").find_next("td").text.strip()
        wifi = specs_list.find("td", text="Wi-Fi").find_next("td").text.strip()
        connection = specs_list.find("td", text="Network").find_next("td").text.strip()
        internal_memory = specs_list.find("td", text="Internal").find_next("td").text.strip()

        info = {
            "processor": processor,
            "battery": battery,
            "ram": ram,
            "wifi": wifi,
            "connection": connection,
            "internal_memory": internal_memory
        }

        return info

