import json

API_TOKEN = "5779105062:AAE0g_K0Cnba2CBO6kkpB1mAS9Rt1xoBRSI"
parameters = {
    "value": 1000,
    "min_spread": 0.5,
    "min_good": 100,
    "max_bad": 0,
    "maker": True
}
exchangers_black = {}
quotes_black = []

with open("quotes.json", "r") as read_file:
    quotes: dict = json.load(read_file)

with open("banks.json", "r") as read_file:
    banks: dict = json.load(read_file)

cotirs = {key: (0, 0) for key in quotes.keys()}
cotirs["USDTRUB"] = (0, 0)