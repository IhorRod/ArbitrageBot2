import asyncio
import time
import config
from config import *
from bestchange_api import BestChange
from numba import jit

def run_bestchange():
    time.sleep(10)
    asyncio.Task(run_bestchange1())


async def run_bestchange1():
    try:
        await asyncio.get_event_loop().run_in_executor(None, update_cots)
    except:
        run_bestchange()

@jit(nopython=True, cache=True)
def calculate(value:float, give: float, get: float, cot_usdt: float, cot_rub: float):
    value_krip = (value / give) * get
    value_usdt = value_krip * cot_usdt
    value_end = value_usdt * cot_rub
    return value_krip, value_usdt, value_end, cot_usdt, cot_rub


def update_cots():
    while True:
        print("start")
        start_time_all = time.time()
        config.list_bestchange = get_cots()
        print("finish all in", time.time() - start_time_all)
        if len(config.list_bestchange) > 20:
            config.list_bestchange = config.list_bestchange[:20]


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

                        if parameters["maker"]==1:
                            temp_calc = calculate(float(parameters['value']), float(k['give']), float(k['get']), cotirs[key_quote][1], cotirs["USDTRUB"][1])
                        else:
                            temp_calc = calculate(float(parameters['value']), float(k['give']), float(k['get']), cotirs[key_quote][0], cotirs["USDTRUB"][0])

                        abs_diff = round(temp_calc[2], 2)
                        diff = round(((abs_diff / float(parameters['value'])) - 1) * 100, 1)
                        # print(i, j, diff, abs_diff)
                        if diff >= parameters['min_spread'] and parameters['value']>=k['min_sum'] and parameters['value']<=k['max_sum']:
                            check = True
                            with open("exchangers.json", "r") as read_file:
                                exchangers_names: dict = json.load(read_file)
                            for f in exchangers_names:
                                if int(exchangers_names[f]) == k["exchange_id"]:
                                    exch_name: str = f
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
                                    'val_usdt': temp_calc[1],
                                    'exch_name': exch_name
                                }
                            )
    lst_temp.sort(key=lambda x: -x['spread_abs'])
    
    temp_dict = {}
    exchangers = api.exchangers().get()
    with open("exchangers.json", 'r') as f:
        temp_dict = json.load(f)
    print("start len", len(temp_dict))
    for i in exchangers:
        data = exchangers[i]
        temp_dict[data['name']] = data['id']
    with open("exchangers.json", 'w') as f:
        json.dump(temp_dict, f)
    print("end len", len(temp_dict))
    
    return lst_temp
