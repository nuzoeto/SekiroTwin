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

    search_results = soup.select(".makers .search-brand-model-name")
    if search_results:
        first_result = search_results[0]
        device_link = first_result['href']
        device_url = f"https://www.gsmarena.com/{device_link}"
        device_response = requests.get(device_url)
        device_soup = BeautifulSoup(device_response.content, "html.parser")

        processor = device_soup.select_one("#specs-list span[data-spec='cpu'] + strong").text.strip()
        battery = device_soup.select_one("#specs-list span[data-spec='batdescription1'] + strong").text.strip()
        ram = device_soup.select_one("#specs-list span[data-spec='internalmemory'] + strong").text.strip()
        wifi = device_soup.select_one("#specs-list span[data-spec='wlan'] + strong").text.strip()
        connection = device_soup.select_one("#specs-list span[data-spec='networkspeed'] + strong").text.strip()
        bluetooth = device_soup.select_one("#specs-list span[data-spec='bluetooth'] + strong").text.strip()

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
