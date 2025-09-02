import requests
import json

inventory = [
    {
        "name": "bigip-a.va-dc1.networkgear.net",
        "ip_address": "10.10.10.10",
        "location": "Virginia DC1",
        "state": "ONLINE",
        "device_type": "App delivery security platform",
        "make": "F5",
        "model": "r5900",
        "os_version": "17.5.1",
        "end_of_support": "2025-12-31",
    },
    {
        "name": "bigip-b.va-dc1.networkgear.net",
        "ip_address": "10.10.10.11",
        "location": "Virginia DC1",
        "state": "ONLINE",
        "device_type": "App delivery security platform",
        "make": "F5",
        "model": "r5900",
        "os_version": "17.5.1",
        "end_of_support": "2025-12-31",
    },
]


def fetch_inventory():
    url = "http://127.0.0.1:8000/inventory/api/"
    response = requests.get(url)
    data = response.json()
    print(json.dumps(data, indent=4))


def create_inventory(payload):
    url = "http://127.0.0.1:8000/inventory/api/"
    response = requests.post(url, json=payload)
    print(response)


if __name__ == "__main__":
    fetch_inventory()
    # for data in inventory:
    # create_inventory(data)
