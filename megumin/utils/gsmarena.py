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
        link = li.a["href"]
        image = li.img["src"]
        id = link.split("-")[0].split("_")[-1]

        result = {
            "name": name,
            "id": id,
            "link": link,
            "image": image
        }
        results.append(result)

    return json.dumps(results)


def device_info(link):
    url = f"https://www.gsmarena.com/{link}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    specs_list = soup.find("div", class_="specs-list")
    if specs_list:
        battery = specs_list.find("span", attrs={"data-spec": "batdescription1"}).find_next_sibling("strong").text.strip()
        processor = specs_list.find("span", attrs={"data-spec": "cpu"}).find_next_sibling("strong").text.strip()
        ram = specs_list.find("span", attrs={"data-spec": "internalmemory"}).find_next_sibling("strong").text.strip()
        connection = specs_list.find("span", attrs={"data-spec": "networkspeed"}).find_next_sibling("strong").text.strip()
        wifi = specs_list.find("span", attrs={"data-spec": "wlan"}).find_next_sibling("strong").text.strip()
        internal_memory = specs_list.find("span", attrs={"data-spec": "internalmemory"}).find_next_sibling("strong").text.strip()

        info = {
            "battery": battery,
            "processor": processor,
            "ram": ram,
            "connection": connection,
            "wifi": wifi,
            "internal_memory": internal_memory
        }

        return json.dumps(info)

    return None

