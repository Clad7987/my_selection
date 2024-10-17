import pathlib
import os
import json
import datetime


def main(obj=None, is_first_run=True):
    data_path = pathlib.Path("./data")
    data_path.mkdir(exist_ok=True)
    path = pathlib.Path("./imgs")
    if is_first_run:
        data = {"images": []}
        for image in os.listdir(path):
            data["images"].append(
                {
                    "path": str(path / image),
                    "create_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }
            )

        with open(data_path / "data.json", "w") as file:
            json.dump(data, file)
    else:
        with open(data_path / "data.json", "r") as file:
            data = json.load(file)

        for item in obj:
            data["images"].append(
                {
                    "path": str(path / item.get("filename")),
                    "create_at": item.get("date"),
                }
            )

        with open(data_path / "data.json", "w") as file:
            json.dump(data, file)


if __name__ == "__main__":
    main()
