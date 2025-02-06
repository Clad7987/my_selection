import json
import os
import cv2

root = 'imgs'

join = lambda curr,path: os.path.join(curr,path)

folders = [join(root, folder) for folder in os.listdir(root)]

full_data = {"Sem categoria": []}
for item in folders:
    if os.path.isdir(item):
        full_data[os.path.basename(item)] = []
        for file in os.listdir(item):
            path = join(item, file)
            print(path)
            img = cv2.imread(path)
            size = img.shape[:2]

            full_data[os.path.basename(item)].append([path, *size])
    else:
        if item.endswith('mp4'):
            full_data['Sem categoria'].append([item, 0, 0])
        else:
            full_data['Sem categoria'].append([item, *[cv2.imread(item).shape[:2]]])

with open('data/data2.0.json', "w") as file:
    json.dump(full_data, file)
