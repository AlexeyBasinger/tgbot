import math

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.markdown import hcode
from tgbot.payment.QIWI import db
from tgbot.db_api.FSM import oplata_ru
from tgbot.keyboards.inline import cancel_inline_button, menu
from tgbot.payment.QIWI import p2p
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def dostavka_dannie(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.delete()
    if call.data[10:] in hcode(await db.pokasi_id()):
        await oplata_ru.amount.set()
        async with state.proxy() as data:
            data['tovar_id'] = int(call.data[10:])
        await call.message.answer('Укажите количество товара', reply_markup=cancel_inline_button)


async def amount_tovara(message: Message, state: FSMContext):
    try:
        data = await state.get_data()
        if int(message.text) <= await db.amount_tovarov(tovar_id=data.get('tovar_id')):
            async with state.proxy() as data:
                data['amount'] = int(message.text)
                await oplata_ru.next()
                await message.answer('Введите адрес доставки\n'
                                     'Город,улицу,дом', reply_markup=cancel_inline_button)
        elif await db.amount_tovarov(tovar_id=data.get('tovar_id')) == 0:
            await message.answer('Данный товар закончился(')
        else:
            await message.answer(f'Товаров на складе: {await db.amount_tovarov(tovar_id=data.get("tovar_id"))}')
    except ValueError:
        await message.answer('Введите только число!')


async def dostavka_street(message: Message, state: FSMContext):
    data = await state.get_data()
    comment = message.from_user.id
    total = await db.price_tovar_select(data.get('tovar_id')) * data.get('amount')
    skidka = 0
    skidka_db = await db.poluchit_skidka(message.from_user.id)
    if skidka_db:
        skidka += skidka_db * 100
        if total - skidka > 0:
            total -= skidka
            async with state.proxy() as data:
                data['skidka'] = 0
        else:
            skidka -= total
            total = 1
            skidka = math.floor(skidka / 100)
            async with state.proxy() as data:
                data['skidka'] = skidka

    bill = p2p.bill(amount=total, lifetime=10,
                    comment=comment)
    await db.insert_in_tovar_oplata(user_id=message.from_user.id, tovar_id=data.get('tovar_id'),
                                    amount=data.get('amount'), deliviry=message.text, oplata_state=0,
                                    bill_id=str(bill.bill_id))
    await message.answer('Осталось оплатить товар\nСкидка за рефералов применяется автоматически\nно товар не может '
                         'стоить меньше рубля', reply_markup=InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text='Оплатить', url=bill.pay_url)],
                         [InlineKeyboardButton(text='Проверить оплату', callback_data=f'check_{bill.bill_id}')],
                         [InlineKeyboardButton(text='❌Отмена', callback_data='otmena_pls')]]))


async def provekra_pay(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=10)
    data = await state.get_data()
    bill = call.data[6:]
    info = await db.check_bill_id(bill)
    if info != False:
        if str(p2p.check(bill_id=bill).status) == 'PAID':
            await call.message.delete()
            await call.message.answer('Товар успешно оплачен\n'
                                      'Доставка будет реализована в течении 5 дней\n'
                                      'Обратная связь по телефону +79165502550', reply_markup=menu)
            await db.update_price(bill)
            a = list(await db.oplata_set_state(bill))
            await db.update_amount_tovarov(a[0], a[1])
            await db.dobavit_skidku(call.from_user.id, data.get('skidka'))



            await state.finish()
        else:
            await call.message.answer('Вы не оплатили счет')
    else:
        await call.message.answer('Оплата не найдена')


def register_all_oplata_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(dostavka_dannie, text_contains='buy_tovar_')
    dp.register_message_handler(amount_tovara, state=oplata_ru.amount)
    dp.register_message_handler(dostavka_street, state=oplata_ru.street)
    dp.register_callback_query_handler(provekra_pay, text_contains='check_', state=oplata_ru.street)
