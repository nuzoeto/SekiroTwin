import requests
from bs4 import BeautifulSoup
import json

def search(query):
    url = f"https://www.gsmarena.com/results.php3?sQuickSearch=yes&sName={query}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

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

    return result

def device_info(link):
    url = f"https://www.gsmarena.com/{link}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    processor = soup.select_one("#specs-list span[data-spec='cpu'] + strong").text.strip()
    battery = soup.select_one("#specs-list span[data-spec='batdescription1'] + strong").text.strip()
    ram = soup.select_one("#specs-list span[data-spec='internalmemory'] + strong").text.strip()
    wifi = soup.select_one("#specs-list span[data-spec='wlan'] + strong").text.strip()
    connection = soup.select_one("#specs-list span[data-spec='networkspeed'] + strong").text.strip()
    bluetooth = soup.select_one("#specs-list span[data-spec='bluetooth'] + strong").text.strip()

    info = {
        "processor": processor,
        "battery": battery,
        "ram": ram,
        "wifi": wifi,
        "connection": connection,
        "bluetooth": bluetooth
    }

    return info


