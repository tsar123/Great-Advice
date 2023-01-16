import json
import requests as requests
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import executor

from auth_bot import token


def api_test(url):
    req = requests.get(f"{url}")
    data = req.content.decode()
    req.close()
    dictFull = json.loads(data)
    return dictFull["text"]


def telegramBot():
    bot = Bot(token=token)
    dp = Dispatcher(bot)
    keyboard = [['Рандомный совет', 'Совет дня'],
                ['Предложить совет', 'Магазин']]
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)
    dictLink = {'offer': 'https://fucking-great-advice.ru/add', 'full': 'https://fucking-great-advice.ru/'}
    dictText = {'offer': 'Предложить совет!', 'full': 'Полная версия'}

    def button(text, link):
        key = InlineKeyboardMarkup(row_width=1)
        key.insert(InlineKeyboardButton(text=text, url=link))
        return key

    @dp.message_handler(commands=["start"])
    async def startingMessage(message: types.Message):
        await message.answer("***Содержит ненормативную лексику!***\nПрисылает рандомный охуенный совет!\nПростое решение в виде tg-бота добавит в Вашу жизнь чертову гору мотивации и сделает Ваш день более продуктивным.\nОхуенный блять совет — каждый день.\nА по пятницам — охуительный!", reply_markup=markup)

    @dp.message_handler(commands=["day"])
    async def adviceDay(message: types.Message):
        await message.answer(api_test("https://fucking-great-advice.ru/api/latest"))

    @dp.message_handler(commands=["random"])
    async def adviceRandom(message: types.Message):
        await message.answer(api_test("https://fucking-great-advice.ru/api/random"))

    @dp.message_handler(commands=["shop"])
    async def shop(message: types.Message):
        await message.answer('Магазин охуенного мерча: https://shop.fucking-great-advice.ru/')

    @dp.message_handler(commands=["offer"])
    async def adviceOffer(message: types.Message):
        await message.answer("Собираем советы по крупинкам со всего света. Внести и ты кусочек своей мудрости, ёпта!", reply_markup=button(dictText['offer'], dictLink['offer']))

    @dp.message_handler(commands=["full"])
    async def fullVersion(message: types.Message):
        await message.answer("Полная версия охуенного блять совета! Больше советов в других форматах!", reply_markup=button(dictText['full'], dictLink['full']))

    @dp.message_handler(commands=["about"])
    async def about(message: types.Message):
        await message.answer('О нас:\nСоветы берутся из сайта: https://fucking-great-advice.ru/\nTg-бота скрафтил: @tsaregorodtsevg')

    @dp.message_handler(commands=["rkn"])
    async def nadzor(message: types.Message):
        await message.answer('Дорогой Роскомнадзор!\nСайт не является средством массовой информации.\nКонтент данного сайта предназначен для возрастной категории посетителей «18+», в соответствии с требованиями Федерального закона от 29 декабря 2010 г. № 436-ФЗ «О защите детей от информации, причиняющей вред их здоровью и развитию» (с изменениями и дополнениями) в ред. Федерального закона от 28.07.2012 № 139-ФЗ.\n\nВсего хорошего.')

    async def keyboardMenu(message: types.Message):
        match message.text:
            case "Рандомный совет":
                await message.answer(api_test("https://fucking-great-advice.ru/api/random"))
            case "Предложить совет":
                await message.answer("Собираем советы по крупинкам со всего света. Внести и ты кусочек своей мудрости, ёпта!", reply_markup=button(dictText['offer'], dictLink['offer']))
            case "Магазин":
                await message.answer('Магазин охуенного мерча: https://shop.fucking-great-advice.ru/')
            case "Сделать картинку":
                await message.answer('Напиши эту охуенную фразу!')
            case "Совет дня":
                await message.answer(api_test("https://fucking-great-advice.ru/api/latest"))

    dp.register_message_handler(keyboardMenu, state=None)
    executor.start_polling(dp, skip_updates=True)


if __name__ == '__main__':
    # api_test("https://fucking-great-advice.ru/api/random") #рандомный совет
    # api_test("https://fucking-great-advice.ru/api/latest") #совет дня
    "https://fucking-great-advice.ru/add"  # предложить совет
    "https://shop.fucking-great-advice.ru/"  # купить мерч
    telegramBot()
