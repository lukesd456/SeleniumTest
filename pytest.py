import json

data = {
    "data" : 'fsá'
}

with open('data.json', "w", encoding='utf-') as file:
    json.dump(data, file, ensure_ascii=False)