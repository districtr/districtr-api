import json
import sys

import requests


def main(path):
    with open(path) as f:
        places = json.load(f)

    places_from_api = requests.get("https://api.districtr.org/places/").json()
    places_by_name = {place["name"]: place for place in places_from_api}

    for place in places:
        place_from_api = places_by_name[place["name"]]
        place["permalink"] = place["id"]
        place["id"] = place_from_api["id"]
        place["description"] = place_from_api["description"]

    with open(path, "w") as f:
        json.dump(places, f)


if __name__ == "__main__":
    main(sys.argv[1])
