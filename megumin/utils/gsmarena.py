import requests
from bs4 import BeautifulSoup
import json
import uuid
import asyncio

def device_info(url):
    gid = uuid.uuid4()
    headeris = {
        "User-Agent": f"Dalvik/2.1.0 (Linux; U; Android 13; {gid}/gsmarena Build/SQ1D.211205.017)"
    }
    response = requests.get(url, headers=headeris)
    soup = BeautifulSoup(response.content, "html.parser")

    device_json = {}

    # Verifica se as informações do dispositivo estão disponíveis
    specs_list = soup.find("div", class_="specs-list")
    if specs_list:
        # Obtém as informações desejadas
        processor = specs_list.find("span", attrs={"data-spec": "cpu"})
        device_json["processor"] = processor.find_next_sibling("strong").text.strip() if processor else None

        ram = specs_list.find("span", attrs={"data-spec": "internalmemory"})
        device_json["ram"] = ram.find_next_sibling("strong").text.strip() if ram else None

        internal_storage = specs_list.find("span", attrs={"data-spec": "rom"})
        device_json["internal_storage"] = internal_storage.find_next_sibling("strong").text.strip() if internal_storage else None

        battery = specs_list.find("span", attrs={"data-spec": "batdescription1"})
        device_json["battery"] = battery.find_next_sibling("strong").text.strip() if battery else None

        description = soup.find("div", class_="section-body")
        device_json["description"] = description.text.strip() if description else None

    return device_json

async def search(query):
    gid = uuid.uuid4()
    headeris = {
        "User-Agent": f"Dalvik/2.1.0 (Linux; U; Android 13; {gid}/gsmarena Build/SQ1D.211205.017)"
    }
    url = f"https://www.gsmarena.com/results.php3?sQuickSearch=yes&sName={query}"
    response = requests.get(url, headers=headeris)
    soup = BeautifulSoup(response.content, "html.parser")

    results = []

    # Verifica se os resultados da pesquisa estão disponíveis
    results_container = soup.find("div", class_="makers")
    if results_container:
        for li in results_container.find_all("li"):
            result = {}

            # Obtém as informações do dispositivo
            result["id"] = li.a["href"].split("-")[0].split("_")[-1]
            result["image"] = li.img["src"]
            result["link"] = li.a["href"]
            result["name"] = li.a.text.strip()

            # Obtém as informações adicionais do dispositivo
            device_url = f"https://www.gsmarena.com/{result['link']}"
            device_info = await asyncio.to_thread(device_info, device_url)
            if device_info:
                result.update(device_info)

            results.append(result)

    return json.dumps(results)
