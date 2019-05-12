import json
import os
import sys

import requests

# API = "https://api.districtr.org"
API = "http://localhost:5000"
TOKEN = os.environ.get("DISTRICTR_API_TOKEN")
HEADERS = {"Authorization": "Bearer " + TOKEN}


def main(path):
    with open(path) as f:
        places = json.load(f)

    for place in places:
        data = convert(place)
        response = requests.post(API + "/places/", headers=HEADERS, json=data)
        print(response)
        if response.status_code >= 200 and response.status_code < 400:
            print(response.json())
        else:
            print(response.text)
            break


def convert(data):
    del data["districtingProblems"]
    del data["units"]
    data["slug"] = data["id"]
    del data["slug"]
    return data


if __name__ == "__main__":
    main(sys.argv[1])
