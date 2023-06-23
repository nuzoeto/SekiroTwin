import requests
from bs4 import BeautifulSoup
import json
import uuid

import requests
from bs4 import BeautifulSoup
import json

def device_info(url):
    gid = uuid.uuid4()
    headers = {
        "User-Agent": f"Dalvik/2.1.0 (Linux; U; Android 13; {gid}/gsmarena Build/SQ1D.211205.017)"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    device_info = {}

    # Verifica se as informações do dispositivo estão disponíveis
    specs_list = soup.find("div", class_="specs-list")
    if specs_list:
        # Obtém as informações desejadas
        device_info["processor"] = specs_list.find("span", attrs={"data-spec": "cpu"}).find_next_sibling("strong").text.strip()
        device_info["ram"] = specs_list.find("span", attrs={"data-spec": "internalmemory"}).find_next_sibling("strong").text.strip()
        device_info["internal_storage"] = specs_list.find("span", attrs={"data-spec": "rom"}).find_next_sibling("strong").text.strip()
        device_info["battery"] = specs_list.find("span", attrs={"data-spec": "batdescription1"}).find_next_sibling("strong").text.strip()
        device_info["description"] = soup.find("div", class_="section-body").text.strip()

    return device_info

def search(query):
    url = f"https://www.gsmarena.com/results.php3?sQuickSearch=yes&sName={query}"
    gid = uuid.uuid4()
    headers = {
        "User-Agent": f"Dalvik/2.1.0 (Linux; U; Android 13; {gid}/gsmarena Build/SQ1D.211205.017)"
    }
    response = requests.get(url, headers=headers)
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
            device_info = device_info(device_url)
            if device_info:
                result.update(device_info)

            results.append(result)

    return json.dumps(results)



