import requests
from bs4 import BeautifulSoup
import json

def search(query: str):
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

    return json.dumps(results)


def device_info(link: str):
    url = f"https://www.gsmarena.com/{link}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    specs_list = soup.find("div", class_="specs-list")
    if specs_list:
        processor = specs_list.find("span", attrs={"data-spec": "cpu"}).find_next_sibling("strong").text.strip()
        battery = specs_list.find("span", attrs={"data-spec": "batdescription1"}).find_next_sibling("strong").text.strip()
        ram = specs_list.find("span", attrs={"data-spec": "internalmemory"}).find_next_sibling("strong").text.strip()
        wifi = specs_list.find("span", attrs={"data-spec": "wlan"}).find_next_sibling("strong").text.strip()
        connection = specs_list.find("span", attrs={"data-spec": "networkspeed"}).find_next_sibling("strong").text.strip()
        bluetooth = specs_list.find("span", attrs={"data-spec": "bluetooth"}).find_next_sibling("strong").text.strip()

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
