import pathlib
import os
import json
import datetime


def main(obj=None, is_first_run=True):
    data_path = pathlib.Path("./data")
    data_path.mkdir(exist_ok=True)
    path = pathlib.Path("./imgs")
    if is_first_run:
        data = {
            "tumblr": {"images": [], "videos": []},
            "reddit": {"images": [], "videos": []},
            "unknow": {"images": [], "videos": []},
        }

        for item in os.listdir(data_path):
            if "tumblr" in item.get("filename").lower():
                if "mp4" in item.get("filename").lower():
                    data["tumblr"]["videos"].append(
                        {
                            "path": str(path / item.get("filename")),
                            "create_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "type": "video",
                        }
                    )
                else:
                    data["tumblr"]["images"].append(
                        {
                            "path": str(path / item.get("filename")),
                            "create_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "type": "image",
                        }
                    )
            elif "rdt" in item.get("filename").lower():
                if "mp4" in item.get("filename").lower():
                    data["reddit"]["videos"].append(
                        {
                            "path": str(path / item.get("filename")),
                            "create_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "type": "video",
                        }
                    )
                else:
                    data["reddit"]["images"].append(
                        {
                            "path": str(path / item.get("filename")),
                            "create_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "type": "image",
                        }
                    )
            else:
                if "mp4" in item.get("filename").lower():
                    data["unknow"]["videos"].append(
                        {
                            "path": str(path / item.get("filename")),
                            "create_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "type": "video",
                        }
                    )
                else:
                    data["unknow"]["images"].append(
                        {
                            "path": str(path / item.get("filename")),
                            "create_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "type": "image",
                        }
                    )

        with open(data_path / "data.json", "w") as file:
            json.dump(data, file)
    else:
        with open(data_path / "data.json", "r") as file:
            data = json.load(file)

        for item in obj:
            if "tumblr" in item.get("filename").lower():
                if "mp4" in item.get("filename").lower():
                    data["tumblr"]["videos"].append(
                        {
                            "path": str(path / item.get("filename")),
                            "create_at": item.get("date"),
                            "type": "video",
                        }
                    )
                else:
                    data["tumblr"]["images"].append(
                        {
                            "path": str(path / item.get("filename")),
                            "create_at": item.get("date"),
                            "type": "image",
                        }
                    )
            elif "rdt" in item.get("filename").lower():
                if "mp4" in item.get("filename").lower():
                    data["reddit"]["videos"].append(
                        {
                            "path": str(path / item.get("filename")),
                            "create_at": item.get("date"),
                            "type": "video",
                        }
                    )
                else:
                    data["reddit"]["images"].append(
                        {
                            "path": str(path / item.get("filename")),
                            "create_at": item.get("date"),
                            "type": "image",
                        }
                    )
            else:
                if "mp4" in item.get("filename").lower():
                    data["unknow"]["videos"].append(
                        {
                            "path": str(path / item.get("filename")),
                            "create_at": item.get("date"),
                            "type": "video",
                        }
                    )
                else:
                    data["unknow"]["images"].append(
                        {
                            "path": str(path / item.get("filename")),
                            "create_at": item.get("date"),
                            "type": "image",
                        }
                    )

        with open(data_path / "data.json", "w") as file:
            json.dump(data, file)

        import util

        util.remove_duplicated()


if __name__ == "__main__":
    main()
