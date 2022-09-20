import asyncio
import json

from aiogram.dispatcher.filters import Text

#from bestchange_listener import run_bestchange
from config import *
from aiogram import Bot, Dispatcher, executor, types
#from binance_connect import start_listening
from keyboards import *
from States import StatesChange
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import config

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


async def update(id) -> int:
    text_quote = "1. USDT->{}\n" \
                 "Покупка по маркету за: {}\n" \
                 "Ссылка:{}\n" \
                 "2. {}->{}\n" \
                 "Курс обмена: {} {} на {} {}\n" \
                 "Отдаете примерно: {} {}\n" \
                 "Получаете примерно: {} {}\n" \
                 "Ссылка на обменник: {}\n" \
                 "3. {}->USDT\n" \
                 "Продажа по маркету: {}\n" \
                 "Ссылка:{}\n\n" \
                 "Итоговая сумма: {} USDT\n" \
                 "Процентный спред: {}%"
    if len(config.list_bestchange) != 0:
        for i in config.list_bestchange:
            await bot.send_message(id,
                                   text=text_quote.format(
                                       i['from'], i['buy'],
                                       "https://www.binance.com/ru-UA/trade/{}_USDT?theme=dark&type=spot"
                                       .format(i['from']),
                                       i['from'], i['to'],
                                       i['give'], i['from'], i['get'], i['to'],
                                       i['from_val'], i['from'],
                                       i['to_val'], i['to'],
                                       i['link'],
                                       i['to'], i['sell'],
                                       "https://www.binance.com/ru-UA/trade/{}_USDT?theme=dark&type=spot"
                                       .format(i['to']),
                                       i['spread_abs'], i['spread_proc']))
    return len(config.list_bestchange)


async def updates(id):
    while True:
        await update(id)
        await asyncio.sleep(60)


def main():
    executor.start_polling(dp, skip_updates=True)


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer("Добро пожаловать в бота который сканирует Бестчендж и Бинанс, находя связки",
                         reply_markup=keyboard_main)


@dp.callback_query_handler(lambda c: c.data == "add_exchanger")
async def process_addexchanger(callback_query: types.CallbackQuery):
    state = dp.current_state(chat=callback_query.message.chat.id, user=callback_query.from_user.id)
    await bot.send_message(callback_query.from_user.id,
                           text="Введите ID обменника, который хотите убрать из ЧС:",
                           reply_markup=keyboard_cancel)
    await state.set_state(StatesChange.STATE_ADD_EXCHANGER)
    await callback_query.message.delete()


@dp.callback_query_handler(lambda c: c.data == "diff_exchanger")
async def process_diffexchanger(callback_query: types.CallbackQuery):
    state = dp.current_state(chat=callback_query.message.chat.id, user=callback_query.from_user.id)
    await bot.send_message(callback_query.from_user.id,
                           text="Введите название обменника, который хотите добавить в ЧС:",
                           reply_markup=keyboard_cancel)
    await state.set_state(StatesChange.STATE_DIFF_EXCHANGER)
    await callback_query.message.delete()


@dp.callback_query_handler(lambda c: c.data == "add_quotes")
async def process_addquotes(callback_query: types.CallbackQuery):
    state = dp.current_state(chat=callback_query.message.chat.id, user=callback_query.from_user.id)
    await bot.send_message(callback_query.from_user.id,
                           text="Введите название криптовалюты, которую хотите убрать из ЧС:",
                           reply_markup=keyboard_cancel)
    await state.set_state(StatesChange.STATE_ADD_QUOTE)
    await callback_query.message.delete()


@dp.callback_query_handler(lambda c: c.data == "diff_quotes")
async def process_diffquotes(callback_query: types.CallbackQuery):
    state = dp.current_state(chat=callback_query.message.chat.id, user=callback_query.from_user.id)
    await bot.send_message(callback_query.from_user.id,
                           text="Введите название криптовалюты, которую хотите добавить в ЧС:",
                           reply_markup=keyboard_cancel)
    await state.set_state(StatesChange.STATE_DIFF_QUOTE)
    await callback_query.message.delete()


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('change'))
async def process_change(callback_query: types.CallbackQuery):
    regime = callback_query.data[7:]
    state = dp.current_state(chat=callback_query.message.chat.id, user=callback_query.from_user.id)
    if regime == "value":
        await bot.send_message(callback_query.from_user.id,
                               text="Введите новую рабочую сумму:",
                               reply_markup=keyboard_cancel)
        await state.set_state(StatesChange.STATE_VALUE)

    if regime == "min_spread":
        await bot.send_message(callback_query.from_user.id,
                               text="Введите новую минимальную доходность:",
                               reply_markup=keyboard_cancel)
        await state.set_state(StatesChange.STATE_SPREAD)
    if regime == "min_good":
        await bot.send_message(callback_query.from_user.id,
                               text="Введите новое количество минимально хороших комментариев:",
                               reply_markup=keyboard_cancel)
        await state.set_state(StatesChange.STATE_MIN_GOOD)
    if regime == "max_bad":
        await bot.send_message(callback_query.from_user.id,
                               text="Введите максимальное количество плохих комментариев:",
                               reply_markup=keyboard_cancel)
        await state.set_state(StatesChange.STATE_MAX_BAD)
    await callback_query.message.delete()


@dp.callback_query_handler(lambda c: c.data == "add_exchanger", state=StatesChange.STATE_EMPTY)
async def process_addexchanger1(callback_query: types.CallbackQuery):
    await process_addexchanger(callback_query)


@dp.callback_query_handler(lambda c: c.data == "diff_exchanger", state=StatesChange.STATE_EMPTY)
async def process_diffexchanger1(callback_query: types.CallbackQuery):
    await process_diffexchanger(callback_query)


@dp.callback_query_handler(lambda c: c.data == "add_quotes", state=StatesChange.STATE_EMPTY)
async def process_addquotes1(callback_query: types.CallbackQuery):
    await process_addquotes(callback_query)


@dp.callback_query_handler(lambda c: c.data == "diff_quotes", state=StatesChange.STATE_EMPTY)
async def process_diffquotes1(callback_query: types.CallbackQuery):
    await process_diffquotes(callback_query)


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('change'), state=StatesChange.STATE_EMPTY)
async def process_change1(callback_query: types.CallbackQuery):
    await process_change(callback_query)


@dp.message_handler(Text(equals="Включить постоянное обновление📖"))
async def all_updater(message: types.Message):
    text = "Бот начинает работу по поиску связок, поиск производится примерно раз в минуту\n" \
           "Изменять настройки можно прямо во время работы бота, они сразу же применяются.\n" \
           "Удачи в поиске связок!"
    await message.answer(text=text)
    asyncio.Task(updates(message.chat.id))


@dp.message_handler(Text(equals="Настройки⚙️"))
async def parameters_get(message: types.Message):
    temp_text = "Настройки бота на сейчас:\n" \
                "Сумма для работы: {} USDT\n" \
                "Минимальная доходность: {}%\n" \
                "Минимальное кол-во положительных комментариев: {}\n" \
                "Максимальное кол-во отрицательных комментариев: {}\n" \
                "На бирже как мейкер: {}"
    temp_text = temp_text.format(parameters["value"],
                                 parameters["min_spread"],
                                 parameters["min_good"],
                                 parameters["max_bad"],
                                 "Да" if parameters["max_bad"] else "Нет")
    await message.answer(temp_text, reply_markup=keyboard_inline_properties)


@dp.message_handler(Text(equals="Обновить🔃"))
async def update_get(message: types.Message):
    await message.answer("Начинается поиск связок!")
    num = await update(message.chat.id)
    if num == 0:
        await message.answer("Связки не найдены")


@dp.message_handler(Text(equals="Черный список валют💰️"))
async def quotes_change(message: types.Message):
    temp_text = "Доступные сейчас валюты к работе:\n"
    for i in quotes.keys():
        if i not in quotes_black:
            temp_text += "{}, ".format(i[:-4])
    temp_text = temp_text[:-2] + "\nЧерный список: \n"
    for i in quotes_black:
        temp_text += "{}, ".format(i[:-4])
    temp_text = temp_text[:-2]
    await message.answer(temp_text, reply_markup=keyboard_inline_quoteschange)


@dp.message_handler(Text(equals="Отменить❌"), state='*')
async def cancel_operation(message: types.Message):
    state = dp.current_state(chat=message.chat.id, user=message.from_user.id)
    await state.set_state(StatesChange.STATE_EMPTY)
    await message.answer("Операция отменена", reply_markup=keyboard_main)


@dp.message_handler(Text(equals="Черный список обменников💱"))
async def exchangers_change(message: types.Message):
    temp_text = "Обменники в черном списке:\n" \
                "Название - ID\n"
    for i in exchangers_black:
        temp_text += "{} - {}\n".format(exchangers_black[i], i)
    await message.answer(temp_text, reply_markup=keyboard_inline_exchangerschange)


@dp.message_handler(Text(equals="Включить постоянное обновление📖"), state=StatesChange.STATE_EMPTY)
async def all_updater1(message: types.Message):
    await all_updater(message)


@dp.message_handler(Text(equals="Настройки⚙️"), state=StatesChange.STATE_EMPTY)
async def parameters_get1(message: types.Message):
    await parameters_get(message)


@dp.message_handler(Text(equals="Черный список валют💰️"), state=StatesChange.STATE_EMPTY)
async def quotes_change1(message: types.Message):
    await quotes_change(message)


@dp.message_handler(Text(equals="Черный список обменников💱"), state=StatesChange.STATE_EMPTY)
async def exchangers_change1(message: types.Message):
    await exchangers_change(message)


@dp.message_handler(Text(equals="Обновить🔃"), state=StatesChange.STATE_EMPTY)
async def update_get1(message: types.Message):
    await update_get(message)


@dp.message_handler(state=StatesChange.STATE_VALUE)
async def process_value_change(message: types.Message):
    parameters["value"] = int(message.text)
    state = dp.current_state(chat=message.chat.id, user=message.from_user.id)
    await state.set_state(StatesChange.STATE_EMPTY)
    await message.answer("Изменено рабочее количество валюты",
                         reply_markup=keyboard_main)
    await parameters_get(message)


@dp.message_handler(state=StatesChange.STATE_SPREAD)
async def process_value_change(message: types.Message):
    parameters["min_spread"] = float(message.text)
    state = dp.current_state(chat=message.chat.id, user=message.from_user.id)
    await state.set_state(StatesChange.STATE_EMPTY)
    await message.answer("Изменен требуемый минимальный спред",
                         reply_markup=keyboard_main)
    await parameters_get(message)


@dp.message_handler(state=StatesChange.STATE_MIN_GOOD)
async def process_value_change(message: types.Message):
    parameters["min_good"] = int(message.text)
    state = dp.current_state(chat=message.chat.id, user=message.from_user.id)
    await state.set_state(StatesChange.STATE_EMPTY)
    await message.answer("Изменено минимальное количество хороших комментариев",
                         reply_markup=keyboard_main)
    await parameters_get(message)


@dp.message_handler(state=StatesChange.STATE_MAX_BAD)
async def process_value_change(message: types.Message):
    parameters["max_bad"] = int(message.text)
    state = dp.current_state(chat=message.chat.id, user=message.from_user.id)
    await state.set_state(StatesChange.STATE_EMPTY)
    await message.answer("Изменено максимальное количество плохих комментариев",
                         reply_markup=keyboard_main)
    await parameters_get(message)


@dp.message_handler(state=StatesChange.STATE_ADD_QUOTE)
async def process_addquote_read(message: types.Message):
    quote = message.text + "USDT"
    if quote in quotes_black:
        quotes_black.remove(quote)
        await message.answer("Криптовалюта {} убрана из ЧС".format(message.text), reply_markup=keyboard_main)
        state = dp.current_state(chat=message.chat.id, user=message.from_user.id)
        await state.set_state(StatesChange.STATE_EMPTY)
        await quotes_change(message)
    else:
        await message.answer("Нет криптовалюты {} в ЧС".format(message.text))


@dp.message_handler(state=StatesChange.STATE_DIFF_QUOTE)
async def process_diffquote_read(message: types.Message):
    quote = message.text + "USDT"
    if quote in quotes:
        if quote not in quotes_black:
            quotes_black.append(quote)
            await message.answer("Криптовалюта {} добавлена в ЧС".format(message.text), reply_markup=keyboard_main)
            state = dp.current_state(chat=message.chat.id, user=message.from_user.id)
            await state.set_state(StatesChange.STATE_EMPTY)
            await quotes_change(message)
        else:
            await message.answer("Криптовалюта {} уже в ЧС".format(message.text))
    else:
        await message.answer("Нет криптовалюты {} в доступных".format(message.text))


@dp.message_handler(state=StatesChange.STATE_ADD_EXCHANGER)
async def process_addquote_read(message: types.Message):
    exchanger = int(message.text)
    if exchanger in exchangers_black:
        exchangers_black.pop(exchanger)
        await message.answer("Обменник {} убран из ЧС".format(exchanger), reply_markup=keyboard_main)
        state = dp.current_state(chat=message.chat.id, user=message.from_user.id)
        await state.set_state(StatesChange.STATE_EMPTY)
        await exchangers_change(message)
    else:
        await message.answer("Нет обменника {} в ЧС".format(exchanger))


@dp.message_handler(state=StatesChange.STATE_DIFF_EXCHANGER)
async def process_diffquote_read(message: types.Message):
    with open("exchangers.json", "r") as read_file:
        data: dict = json.load(read_file)
    exchanger = message.text
    if data.get(exchanger) != -1:
        if data[exchanger] not in exchangers_black:
            exchangers_black[data[exchanger]] = exchanger
            await message.answer("Обменник {} добавлен в ЧС".format(exchanger), reply_markup=keyboard_main)
            state = dp.current_state(chat=message.chat.id, user=message.from_user.id)
            await state.set_state(StatesChange.STATE_EMPTY)
            await exchangers_change(message)
        else:
            await message.answer("Обменник {} уже в ЧС".format(exchanger))
    else:
        await message.answer("Нет обменника {} в доступных".format(exchanger))


@dp.message_handler(state=StatesChange.STATE_EMPTY)
async def echo(message: types.Message):
    await message.answer("Не знаю такой команды =(")


if __name__ == '__main__':
    #run_bestchange()
    #start_listening()
    main()

'''
print("Start")
    api = BestChange()
    print("Finish")
    temp_dict = {}
    exchangers = api.exchangers().get()
    for i in exchangers:
        data = exchangers[i]
        temp_dict[data['name']] = data['id']
    with open("exchangers.json", 'w') as f:
        json.dump(temp_dict, f)
'''
