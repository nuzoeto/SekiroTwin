import requests
import json

def get_device_info(device_name):
    url = f"https://api.gsmarena.com/devicelist.php3"
    response = requests.get(url)
    devices = response.json()
    
    for device in devices:
        if device["deviceName"].lower() == device_name.lower():
            device_url = device["uri"]
            break
    else:
        return None

    device_info_url = f"https://api.gsmarena.com/{device_url}"
    response = requests.get(device_info_url)
    device_info = response.json()

    return device_info
