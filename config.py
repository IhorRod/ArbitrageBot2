import json
import os
API_TOKEN = os.environ.get("API_TOKEN_SEC")
list_bestchange = []
with open('config.json') as json_file:
    parameters: dict = json.load(json_file)
with open('exch_black.json') as json_file:
    exchangers_black: dict = json.load(json_file)
with open('quotes_black.txt') as f:
    quotes_black: list = f.read().split("\n")
with open('banks_black.txt') as f:
    banks_black: list = f.read().split("\n")
with open("quotes.json", "r") as read_file:
    quotes: dict = json.load(read_file)

with open("banks.json", "r", encoding='utf-8') as read_file:
    banks: dict = json.load(read_file)


cotirs = {key: (0, 0) for key in quotes.keys()}
cotirs["USDTRUB"] = (0, 0)
