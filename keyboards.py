from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

keyboard_empty = ReplyKeyboardMarkup()

keyboard_main = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_main.add(KeyboardButton("Настройки⚙️"), KeyboardButton("Обновить🔃"))
keyboard_main.add(KeyboardButton("Черный список валют💰️"), KeyboardButton("Черный список обменников💱"))
keyboard_main.add(KeyboardButton("Включить постоянное обновление📖"))

keyboard_cancel = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_cancel.add(KeyboardButton("Отменить❌"))

keyboard_inline_properties = InlineKeyboardMarkup()
keyboard_inline_properties.add(InlineKeyboardButton(
    "Изменить рабочую сумму",
    callback_data="change_value"
))
keyboard_inline_properties.add(InlineKeyboardButton(
    "Изменить минимальный доход",
    callback_data="change_min_spread"
))
keyboard_inline_properties.add(InlineKeyboardButton(
    "Изменить мин хороших комментов",
    callback_data="change_min_good"
))
keyboard_inline_properties.add(InlineKeyboardButton(
    "Изменить макс плохих комментов",
    callback_data="change_max_bad"
))

keyboard_inline_quoteschange = InlineKeyboardMarkup()
keyboard_inline_quoteschange.add(InlineKeyboardButton(
    "Добавить криптовалюту в ЧС➕",
    callback_data="diff_quotes"
))
keyboard_inline_quoteschange.add(InlineKeyboardButton(
    "Убрать криптовалюту из ЧС➖",
    callback_data="add_quotes"
))

keyboard_inline_exchangerschange=InlineKeyboardMarkup()
keyboard_inline_exchangerschange.add(InlineKeyboardButton(
    "Добавить обменник в ЧС➕",
    callback_data="diff_exchanger"
))
keyboard_inline_exchangerschange.add(InlineKeyboardButton(
    "Убрать обменник из ЧС➖",
    callback_data="add_exchanger"
))