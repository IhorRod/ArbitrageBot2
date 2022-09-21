import asyncio
import time
import config
from config import *
from bestchange_api import BestChange


def run_bestchange():
    asyncio.Task(run_bestchange1())


async def run_bestchange1():
    await asyncio.get_event_loop().run_in_executor(None, update_cots)


def calculate(give: float, get: float, cot: str):
    value = float(parameters['value'])
    value_krip = (value / give) * get
    if parameters["maker"]:
        cot_usdt = cotirs[cot][1]
        value_usdt = value_krip * cot_usdt
        cot_rub = cotirs["USDTRUB"][1]
        value_end = value_usdt * cot_rub
    else:
        cot_usdt = cotirs[cot][0]
        value_usdt = value_krip * cot_usdt
        cot_rub = cotirs["USDTRUB"][0]
        value_end = value_usdt * cot_rub
    return value_krip, value_usdt, value_end, cot_usdt, cot_rub


def update_cots():
    while True:
        print("start")
        start_time_all = time.time()
        config.list_bestchange = get_cots()
        print("finish all in", time.time() - start_time_all)
        if len(config.list_bestchange) > 5:
            config.list_bestchange = config.list_bestchange[:5]
        print(config.list_bestchange)
        time.sleep(60)


def get_cots():
    start_time = time.time()
    api = BestChange()
    print("finish connect in", time.time() - start_time)
    lst_temp = []
    for key_bank, code_bank in banks.items():
        for key_quote, code_quote in quotes.items():
            if cotirs[key_quote][0] != 0 \
                    and cotirs["USDTRUB"] != 0 \
                    and key_quote not in quotes_black \
                    and key_bank not in banks_black:

                cots = api.rates().filter(
                    code_bank,
                    code_quote
                )
                check = False
                for k in cots:
                    reviews = str(k['reviews']).split('.')
                    if int(reviews[0]) <= parameters['max_bad'] \
                            and int(reviews[1]) >= parameters['min_good'] \
                            and not check \
                            and k['exchange_id'] not in exchangers_black:

                        temp_calc = calculate(float(k['give']), float(k['get']), key_quote)

                        abs_diff = round(temp_calc[2], 2)
                        diff = round(((abs_diff / float(parameters['value'])) - 1) * 100, 1)
                        # print(i, j, diff, abs_diff)
                        if diff >= parameters['min_spread']:
                            check = True
                            lst_temp.append(
                                {
                                    'from': key_bank,
                                    'to': key_quote[:-4],
                                    'spread_abs': abs_diff,
                                    'spread_proc': diff,
                                    'link': "https://www.bestchange.ru/click.php?id={}&from={}&to={}&city=0"
                                    .format(k["exchange_id"], k["give_id"], k["get_id"]),
                                    'sell_krip': temp_calc[3],
                                    'sell_usdt': temp_calc[4],
                                    'give': k['give'],
                                    'get': k['get'],
                                    'val_krip': temp_calc[0],
                                    'val_usdt': temp_calc[1]
                                }
                            )
    lst_temp.sort(key=lambda x: -x['spread_abs'])
    return lst_temp
