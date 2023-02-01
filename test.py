import json

with open('roles.json', 'r', encoding='utf-8') as file:
    file_data = json.load(file)
    for file in file_data:
        print(file)