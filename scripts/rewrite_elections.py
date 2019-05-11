import json
import sys


def main(path, output_path):
    with open(path) as f:
        places = json.load(f)

    for place in places:
        for column_set in place["column_sets"]:
            if column_set["type"] == "election":
                column_set["name"] = "{year} {race}".format(**column_set["metadata"])
                del column_set["metadata"]

    with open(output_path, "w") as f:
        json.dump(places, f)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
