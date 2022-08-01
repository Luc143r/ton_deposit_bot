from config import api_key_bot, admin_id
from request_db import select_user_id, select_deposit, insert_deposit, insert_first_deposit, \
                        select_amount_ton, insert_total_ton, update_total_ton
from parser_ton import parse_currency

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext

import asyncio
import logging
from datetime import date


bot = Bot(token=api_key_bot)
dp = Dispatcher(bot,storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())

#logging.basicConfig(level=logging.INFO)


@dp.message_handler(commands='start')
async def command_start(message: types.Message):

    button_add_deposit = InlineKeyboardButton('Добавить депозит', callback_data="/add_dep")
    button_del_deposit = InlineKeyboardButton('Удалить депозит', callback_data="/del_dep")
    button_view_deposit = InlineKeyboardButton('Баланс', callback_data="/view_dep")
    button_view_rate_ton = InlineKeyboardButton('Посмотреть курс TON', callback_data="/rate_ton")
    button_ton_in_rub = InlineKeyboardButton('TON > RUB', callback_data="/calculate")
    button_help = InlineKeyboardButton('Помощь', callback_data="/help")
    markup_deposit = InlineKeyboardMarkup()
    markup_deposit.row(button_add_deposit, button_del_deposit, button_view_deposit)
    markup_deposit.add(button_view_rate_ton, button_ton_in_rub)
    markup_deposit.add(button_help)

    if select_user_id(message.from_user.id) == 0:
        print('Юзер только только пришел')
        await message.reply(f'Здравствуйте @{message.from_user.username}. Это бот для записи покупки и переводов TON Coin.\nЧтобы поподробнее узнать что я умею, напишите /help', reply_markup=markup_deposit)
    elif select_user_id(message.from_user.id) == 1:
        if message.from_user.id == admin_id:
            await message.reply(f'Привет @{message.from_user.username}. Я надеюсь ты помнишь, что ты являешься администратором?', reply_markup=markup_deposit)
        else:
            await message.reply(f'Здравствуйте, @{message.from_user.username}, я надеюсь Вы помните, что я умею?\nЕсли нет, то введите /help', reply_markup=markup_deposit)

@dp.callback_query_handler(text='/help')
async def callback_help(callback_query: types.CallbackQuery):
    await callback_query.message.answer('Доброго времени суток, пользователь.👋\nВ моем функционале немного функций, предназначенных для учета вложений в TON Coin.🤏\n'
                                        'Все доступные функции осуществляются через меню 👉/start.\n'
                                        '1️⃣Если Вы купили TON и хотите внести данные о покупке, нажмите кнопку "Добавить депозит"\n'
                                        '2️⃣Если Вы продали TON и хотите чтобы из Вашего общего баланса хранящегося во мне внести информацию о продаже, нажмите кнопку "Удалить депозит"\n'
                                        '3️⃣Для просмотра баланса Ваших монет, нажмите кнопку "Баланс"\n'
                                        '4️⃣Также у меня вы можете посмотреть курс TON (данные берутся с CoinMarketCup) и посчитать сколько в данный момент стоят все ваши монеты в рублях согласно курсу.')
    await callback_query.answer()

"""
Create algorithm add deposit
"""
class Add_deposit(StatesGroup):
    amount_ton = State()
    price_ton = State()
    total_price = State()

@dp.callback_query_handler(text='/add_dep')
async def add_deposit(callback_query: types.CallbackQuery):
    await callback_query.message.answer('Отлично, пришлите мне количество TON которые вы купили.\nExample: 9.803171478')
    await callback_query.message.delete()
    await Add_deposit().amount_ton.set()
    await callback_query.answer()

@dp.message_handler(state=Add_deposit.amount_ton)
async def get_price_ton(message: types.Message, state: FSMContext):
    await state.update_data(amount_ton=message.text)
    await message.answer('Продолжим. Теперь пришли мне цену за один TON Coin, по которой ты его купил\nExample: 57.5')
    await Add_deposit.next()

@dp.message_handler(state=Add_deposit.price_ton)
async def get_total_price(message: types.Message, state: FSMContext):
    await state.update_data(price_ton=message.text)
    await message.answer('А теперь пришли мне ту сумму, на которую ты купил TON\nExample: 563.68')
    await Add_deposit.next()

@dp.message_handler(state=Add_deposit.total_price)
async def end_add_deposit(message: types.Message, state: FSMContext):
    if not select_amount_ton(message.from_user.id):
        await state.update_data(total_price=message.text)
        data_deposit = await state.get_data()
        insert_deposit(message.from_user.id, str(date.today()), float(data_deposit["amount_ton"]), float(data_deposit["price_ton"]), float(data_deposit["price_ton"]))
        insert_total_ton(message.from_user.id, float(data_deposit["amount_ton"]))
        await message.answer(f'@{message.from_user.username}, Ваша транзакция добавлена!')
        await state.finish()
    else:
        await state.update_data(total_price=message.text)
        data_deposit = await state.get_data()
        last_total_ton = select_amount_ton(message.from_user.id)[-1][-1]
        total_ton = float(data_deposit['amount_ton']) + float(last_total_ton)
        insert_deposit(message.from_user.id, str(date.today()), float(data_deposit["amount_ton"]), float(data_deposit["price_ton"]), float(data_deposit["total_price"]))
        update_total_ton(message.from_user.id, total_ton)
        await message.answer(f'@{message.from_user.username}, Ваша транзакция добавлена!')
        await state.finish()


"""
Create algorithm add deposit
"""
class Del_deposit(StatesGroup):
    amount_ton = State()

@dp.callback_query_handler(text='/del_dep')
async def add_deposit(callback_query: types.CallbackQuery):
    await callback_query.message.answer('Отправьте количество TON, которое Вы продали.')
    await callback_query.message.answer('Example: 9.375')
    await Del_deposit().amount_ton.set()
    await callback_query.answer()

@dp.message_handler(state=Del_deposit.amount_ton)
async def del_deposit(message: types.Message, state: FSMContext):
    try:
        await state.update_data(amount_ton=message.text)
        data_deposit = await state.get_data()
        last_total_ton = select_amount_ton(message.from_user.id)[-1][-1]
        total_ton = float(last_total_ton) - float(data_deposit['amount_ton'])
        update_total_ton(message.from_user.id, total_ton)
        await message.answer(f'@{message.from_user.username}, изменения внесены.')
        await state.finish()
    except IndexError:
        await message.answer('У вас тут пусто. Удалять нечего...')
        await state.finish()


"""
Function views users deposit
"""
@dp.callback_query_handler(text='/view_dep')
async def view_deposits(callback_query=types.CallbackQuery):
    try:
        total_ton = select_amount_ton(callback_query.from_user.id)[-1][-1]
        await callback_query.message.answer(f'@{callback_query.from_user.username}, вот Ваш баланс: {total_ton} TON')
        await callback_query.answer()
    except IndexError:
        await callback_query.message.answer('Вы пока не добавляли депозиты у меня, поэтому у Вас пока пусто...')
        await callback_query.answer()


"""
Function view rate TON
"""
@dp.callback_query_handler(text='/rate_ton')
async def view_rate_ton(callback_query=types.CallbackQuery):
    await callback_query.message.answer(f'В данный момент курс TON Coin составляет: {parse_currency()}')
    await callback_query.answer()


"""
Function calculate TON to RUB
"""
@dp.callback_query_handler(text='/calculate')
async def calculate_ton(callback_query=types.CallbackQuery):
    calculate_rub = float(parse_currency().split('₽')[-1]) * float(select_amount_ton(callback_query.from_user.id)[-1][-1])
    await callback_query.message.answer(f'@{callback_query.from_user.username}, сейчас Ваши TON стоят: {round(calculate_rub, 2)}')
    await callback_query.answer()

if __name__ == '__main__':
    print('Bot polling')
    executor.start_polling(dp)