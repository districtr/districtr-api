import json
import os
import sys

import requests

API = "https://api.districtr.org"
TOKEN = os.environ.get("DISTRICTR_API_TOKEN")
HEADERS = {"Authorization": "Bearer " + TOKEN}


def main(path):
    with open(path) as f:
        places = json.load(f)

    for place in places:
        serialized_place = {
            "name": place["name"],
            "description": place.get("description", ""),
        }
        response = requests.post(
            API + "/places/", headers=HEADERS, json=serialized_place
        )
        print(response)
        if response.status_code >= 200 and response.status_code < 400:
            print(response.json())
        else:
            print(response.text)
            break


if __name__ == "__main__":
    main(sys.argv[1])
