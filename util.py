import json
from datetime import datetime


def add_propierty(propierty, value):
    with open("data/data.json", "r") as file:
        data = json.load(file)

    for item in data["images"]:
        index = data["images"].index(item)
        data["images"][index][propierty] = value

    with open("data/data.json", "w") as file:
        json.dump(data, file)


def remove_duplicated():
    with open("data/data.json", "r") as file:
        data = json.load(file)

    is_old_data = False
    if is_old_data:
        # Categorize into image and video
        new_data = {}
        new_data["tumblr"] = {
            "images": [
                item
                for item in data["images"]
                if item["type"] == "image" and "tumblr" in item["path"].lower()
            ],
            "videos": [
                item
                for item in data["images"]
                if item["type"] == "video" and "tumblr" in item["path"].lower()
            ],
        }
        new_data["reddit"] = {
            "images": [
                item
                for item in data["images"]
                if item["type"] == "image" and "rdt" in item["path"].lower()
            ],
            "videos": [
                item
                for item in data["images"]
                if item["type"] == "video" and "rdt" in item["path"].lower()
            ],
        }
        new_data["unknow"] = {
            "images": [
                item
                for item in data["images"]
                if item["type"] == "image"
                and (
                    "rdt" not in item["path"].lower()
                    and "tumblr" not in item["path"].lower()
                )
            ],
            "videos": [
                item
                for item in data["images"]
                if item["type"] == "video"
                and (
                    "rdt" not in item["path"].lower()
                    and "tumblr" not in item["path"].lower()
                )
            ],
        }
    else:
        new_data = data

    def filter_oldest(items):
        unique_items = {}
        for item in items:
            path = item["path"]
            create_at = datetime.strptime(item["create_at"], "%Y-%m-%d %H:%M:%S")

            if path in unique_items:
                existing_date = datetime.strptime(
                    unique_items[path]["create_at"], "%Y-%m-%d %H:%M:%S"
                )
                if create_at < existing_date:
                    unique_items[path] = item
            else:
                unique_items[path] = item

        return list(unique_items.values())

    for source in new_data.keys():
        new_data[source]["images"] = filter_oldest(new_data[source]["images"])
        new_data[source]["videos"] = filter_oldest(new_data[source]["videos"])

    with open("data/data.json", "w") as file:
        json.dump(new_data, file)


if __name__ == "__main__":
    remove_duplicated()
