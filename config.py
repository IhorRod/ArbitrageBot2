import json

API_TOKEN = os.environ.get("API_TOKEN1")
parameters = {
    "value": 10000,
    "min_spread": 0,
    "min_good": 100,
    "max_bad": 0,
    "maker": True
}
list_bestchange = []
exchangers_black = {}
quotes_black = []
banks_black = []
with open("quotes.json", "r") as read_file:
    quotes: dict = json.load(read_file)

with open("banks.json", "r", encoding='utf-8') as read_file:
    banks: dict = json.load(read_file)


cotirs = {key: (0, 0) for key in quotes.keys()}
cotirs["USDTRUB"] = (0, 0)
