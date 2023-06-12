from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from bot_app import text, functions


def distributor_keyboard():
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

    distributor_names = functions.all_distributors_name()
    grand = KeyboardButton(text=distributor_names[0])
    meros = KeyboardButton(text=distributor_names[1])

    markup.insert(grand)
    markup.insert(meros)
    return markup


def csv_keyboard():
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

    download_csv = KeyboardButton(text=text.download_csv)
    upload_csv = KeyboardButton(text=text.upload_csv)
    back = KeyboardButton(text=text.back)

    markup.insert(download_csv)
    markup.insert(upload_csv)
    markup.add(back)
    return markup


def upload_keyboard():
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    back = KeyboardButton(text=text.back)
    markup.add(back)
    return markup
