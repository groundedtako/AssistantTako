import json

config = None
# Read the config.json file
with open('config.json', 'r', encoding='utf-8') as file:
    config = json.load(file)
