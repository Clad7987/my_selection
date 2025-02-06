import json
import os

root = 'imgs'

join = lambda curr,path: os.path.join(curr,path)

folders = [join(root, folder) for folder in os.listdir(root)]

full_data = {"Sem categoria": []}
for item in folders:
    if os.path.isdir(item):
        full_data[os.path.basename(item)] = [join(item, file) for file in os.listdir(item)]
    else:
        full_data['Sem categoria'].append(item)

with open('data/data2.0.json', "w") as file:
    json.dump(full_data, file)
