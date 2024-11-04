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


def add_special():
    with open("data/data.json", "r") as file:
        data = json.load(file)

    specials_vids = [
        '<iframe width="854" height="480" src="https://thothub.to/embed/817801" frameborder="0" allowfullscreen></iframe>',
        '<iframe width="222" height="124.875" src="https://thothub.to/embed/43288" frameborder="0" allowfullscreen></iframe>',
        '<iframe width="852" height="480" src="https://thothub.to/embed/809282" frameborder="0" allowfullscreen></iframe>',
        '<iframe width="852" height="480" src="https://thothub.to/embed/840798" frameborder="0" allowfullscreen></iframe>',
        '<iframe width="270" height="151.875" src="https://thothub.to/embed/35490" frameborder="0" allowfullscreen></iframe>',
        '<iframe width="268" height="150.75" src="https://thothub.to/embed/38593" frameborder="0" allowfullscreen></iframe>',
        '<iframe width="852" height="480" src="https://thothub.to/embed/903107" frameborder="0" allowfullscreen></iframe>',
        '<iframe width="852" height="480" src="https://thothub.to/embed/829130" frameborder="0" allowfullscreen></iframe>',
        '<iframe width="270" height="151.875" src="https://thothub.to/embed/518481" frameborder="0" allowfullscreen></iframe>',
        '<iframe width="272" height="153" src="https://thothub.to/embed/901677" frameborder="0" allowfullscreen></iframe>',
        '<iframe width="270" height="151.875" src="https://thothub.to/embed/589638" frameborder="0" allowfullscreen></iframe>',
        '<iframe width="854" height="480" src="https://thothub.to/embed/1184235" frameborder="0" allowfullscreen></iframe>',
        '<iframe width="852" height="480" src="https://thothub.to/embed/250744" frameborder="0" allowfullscreen></iframe>',
        '<iframe width="854" height="480" src="https://thothub.to/embed/571406" frameborder="0" allowfullscreen></iframe>',
        '<iframe width="270" height="151.875" src="https://thothub.to/embed/840354" frameborder="0" allowfullscreen></iframe>',
        '<iframe width="270" height="151.875" src="https://thothub.to/embed/978330" frameborder="0" allowfullscreen></iframe>',
        '<iframe width="852" height="480" src="https://thothub.to/embed/831573" frameborder="0" allowfullscreen></iframe>',
        '<iframe width="854" height="480" src="https://thothub.to/embed/620664" frameborder="0" allowfullscreen></iframe>',
        '<iframe width="854" height="480" src="https://thothub.to/embed/659270" frameborder="0" allowfullscreen></iframe>',
        '<iframe width="852" height="480" src="https://thothub.to/embed/160905" frameborder="0" allowfullscreen></iframe>',
        '<iframe width="852" height="480" src="https://thothub.to/embed/300446" frameborder="0" allowfullscreen></iframe>',
        '<iframe width="850" height="480" src="https://thothub.to/embed/268157" frameborder="0" allowfullscreen></iframe>',
        '<iframe width="270" height="151.875" src="https://thothub.to/embed/933193" frameborder="0" allowfullscreen></iframe>',
        '<iframe width="852" height="480" src="https://thothub.to/embed/270778" frameborder="0" allowfullscreen></iframe>',
        '<iframe width="270" height="151.875" src="https://thothub.to/embed/873539" frameborder="0" allowfullscreen></iframe>',
        '<iframe width="852" height="480" src="https://thothub.to/embed/910824" frameborder="0" allowfullscreen></iframe>',
        '<iframe width="270" height="151.875" src="https://thothub.to/embed/70992" frameborder="0" allowfullscreen></iframe>',
        '<iframe width="270" height="151.875" src="https://thothub.to/embed/789929" frameborder="0" allowfullscreen></iframe>',
        ''
    ]
    specials_imgs = []
    today =  datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data['special'] = {
        "videos": [{"path": vid, "create_at": today, "type": "video"} for vid in specials_vids],
        "images": [{"path": img, "create_at": today, "type": "image"} for img in specials_imgs],
    }

    with open("data/data.json", "w") as file:
        json.dump(data, file)


if __name__ == "__main__":
    # remove_duplicated()
    add_special()
