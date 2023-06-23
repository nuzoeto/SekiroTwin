import requests
from bs4 import BeautifulSoup
import json

def search(query: str):
    url = f"https://www.kimovil.com/en/where-to-buy-{query}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    results = []
    for li in soup.select(".list.grid li"):
        name = li.select_one(".model-info h2").text.strip()
        image = li.select_one(".model-img img")["src"]
        link = li.select_one(".model-img a")["href"]
        id_ = link.split("/")[-1].split("-")[-1]
        result = {
            "name": name,
            "image": image,
            "link": link,
            "id": id_
        }
        results.append(result)

    return results


def device_info(link: str):
    url = f"https://www.kimovil.com{link}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    specs_list = soup.find("div", class_="full-specs")
    if specs_list:
        processor = specs_list.find("th", string="Processor").find_next_sibling("td").text.strip()
        battery = specs_list.find("th", string="Battery").find_next_sibling("td").text.strip()
        ram = specs_list.find("th", string="RAM").find_next_sibling("td").text.strip()
        wifi = specs_list.find("th", string="Wi-Fi").find_next_sibling("td").text.strip()
        connection = specs_list.find("th", string="Network Speed").find_next_sibling("td").text.strip()
        bluetooth = specs_list.find("th", string="Bluetooth").find_next_sibling("td").text.strip()

        info = {
            "processor": processor,
            "battery": battery,
            "ram": ram,
            "wifi": wifi,
            "connection": connection,
            "bluetooth": bluetooth
        }

        return info

    return None

