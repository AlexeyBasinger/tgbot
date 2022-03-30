import re
from asyncio import sleep

import asyncpg
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.utils.markdown import hcode

from tgbot.config import db
from tgbot.keyboards.inline import code, menu_admin, menu_admina_2, cancel_inline_button
from tgbot.payment.QIWI import p2p


async def admin_start(message: Message):
    args = message.get_args()
    if args in hcode(await db.args_id()):
        try:
            b = db.gene_parol()
            while await db.skidka_show_true(b):
                b = db.gene_parol()
            user = await db.add_user(full_name=message.from_user.full_name, username=message.from_user.username,
                                     telegram_id=message.from_user.id, par=b)

            await db.count_referal(int(args))
            await db.count_skidka(int(args))



        except asyncpg.exceptions.UniqueViolationError:
            user = await db.select_user(telegram_id=message.from_user.id)

        await message.answer(f'Поздравляю, вы получили доступ🎉\n'
                             f'Вы можете получить 10 бонусных рублей за каждого преглашонного реферала!!!\n'
                             f'Ваша реферальная ссылка: https://t.me/udemy_exam_bot?start={message.from_user.id}\n'
                             f'Ваш код приглашения: {await db.priglos_id(telegram_id=int(args))}\n',
                             reply_markup=menu_admin)




    else:
        await message.answer('❌Ошибка❌\n'
                             '🔒У вас нет доступа!!!\n'
                             'Чтобы использывать бота введите код приглашения,\n'
                             'либо пройдите по реферальной ссылке\n'
                             f'Если вас никто не пригласил, то просто подпишись на данный канал: https://t.me/testUdemyCors\n'
                             f'Затем нажми на кнопку проверить подписку', reply_markup=code)


async def wait_code_admin(message: Message, state: FSMContext):
    if message.text in hcode(await db.vse_paroli()):
        try:
            b = db.gene_parol()
            while await db.skidka_show_true(b):
                b = db.gene_parol()
            user = await db.add_user(full_name=message.from_user.full_name, username=message.from_user.username,
                                     telegram_id=message.from_user.id, par=b)
            await db.count_referal2(message.text)
            await db.count_skidka2(message.text)


        except asyncpg.exceptions.UniqueViolationError:
            user = await db.select_user(telegram_id=message.from_user.id)

        await message.answer('🎉Поздравляю, вы получили доступ🎉\n'
                             'Вы можете получить 10 бонусных доларов за каждого преглашонного реферала!!!\n'
                             f'Ваша реферальная ссылка: https://t.me/udemy_exam_bot?start={message.from_user.id}\n'
                             f'Ваш код приглашения: {await db.priglos_id(message.from_user.id)}\n',
                             reply_markup=menu_admin)


    else:
        await message.answer('❌Ошибка❌\n'
                             '🔒У вас нет доступа!!!\n'
                             'Чтобы использывать бота введите код приглашения,\n'
                             'либо пройдите по реферальной ссылке\n'
                             f'Если вас никто не пригласил, то просто подпишись на данный канал: https://t.me/testUdemyCors\n'
                             f'Затем нажми на кнопку проверить подписку', reply_markup=code)
    await state.finish()


async def nasad_v_menu_admin(call: CallbackQuery):
    await call.answer()
    await call.message.edit_text(f'🎉Поздравляю, вы получили доступ🎉\n'
                                 f'Вы можете получить 10 бонусных рублей за каждого преглашонного реферала!!!\n'
                                 f'Ваша реферальная ссылка: https://t.me/udemy_exam_bot?start={call.from_user.id}\n'
                                 f'Ваш код приглашения: {await db.priglos_id(call.from_user.id)}',
                                 reply_markup=menu_admin)


async def otmena_admin(call: CallbackQuery, state=FSMContext):
    cur_state = await state.get_state()
    if cur_state is None:
        return
    await state.finish()
    await call.message.delete()
    await call.message.answer('❌Операция была отменена', reply_markup=menu_admin)
    await call.answer()


async def panel_administrator(call: CallbackQuery):
    await call.answer()
    await call.message.edit_text('🎛Административная панель')
    await call.message.edit_reply_markup(menu_admina_2)


async def rassilka_waiting(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.set_state('text_rassilki')
    await call.message.edit_text('Введите текст рассылки', reply_markup=cancel_inline_button)


async def rassilka_go(message: Message, state: FSMContext):
    text = message.text
    users = await db.select_all_users()
    for user in users:
        try:
            await message.bot.send_message(chat_id=user[3], text=text)
            await sleep(0.3)
        except Exception:
            pass
    await state.finish()
    await message.answer('Рассылка окончена', reply_markup=menu_admin)


async def proverka_subscribe_admin(call: CallbackQuery):
    await call.answer()
    state = await call.bot.get_chat_member(chat_id=-1001703741168, user_id=call.from_user.id)
    if state.is_chat_member():
        try:
            b = db.gene_parol()
            while await db.skidka_show_true(b):
                b = db.gene_parol()
            user = await db.add_user(full_name=call.from_user.full_name, username=call.from_user.username,
                                     telegram_id=call.from_user.id, par=b)
        except asyncpg.exceptions.UniqueViolationError:
            user = await db.select_user(telegram_id=call.from_user.id)

        await call.message.edit_text(f'Поздравляю, вы получили доступ🎉\n'
                                     f'Вы можете получить 10 бонусных доларов за каждого приглашенного реферала!!!\n'
                                     f'Ваша реферальная ссылка: https://t.me/udemy_exam_bot?start={call.from_user.id}\n'
                                     f'Ваш код приглашения: {await db.priglos_id(telegram_id=call.from_user.id)}\n',
                                     reply_markup=menu_admin)
    else:
        await call.message.answer('❌Ошибка❌\n'
                                  '🔒У вас нет доступа!!!\n'
                                  'Чтобы использывать бота введите код приглашения,\n'
                                  'либо пройдите по реферальной ссылке\n'
                                  f'Если вас никто не пригласил, то просто подпишись на данный канал: https://t.me/testUdemyCors\n'
                                  f'Затем нажми на кнопку проверить подписку', reply_markup=code)


async def provekra_pay_admin(call: CallbackQuery):
    await call.answer(cache_time=10)
    bill = call.data[6:]
    info = await db.check_bill_id(bill)
    if info != False:
        if str(p2p.check(bill_id=bill).status) == 'PAID':
            await call.message.delete()
            await call.message.answer('Товар успешно оплачен\n'
                                      'Доставка будет реализована в течении 5 дней\n'
                                      'Обратная связь по телефону +79165502550', reply_markup=menu_admin)
            await db.update_price(bill)
            a = list(await db.oplata_set_state(bill))
            await db.update_amount_tovarov(a[0], a[1])
        else:
            await call.message.answer('Вы не оплатили счет')
    else:
        await call.message.answer('Оплата не найдена')


def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin_start, CommandStart(deep_link=re.compile(r"^[0-9]{4,15}$")), is_admin=True)
    dp.register_message_handler(wait_code_admin, state='code', is_admin=True)
    dp.register_callback_query_handler(nasad_v_menu_admin, text='nasad_pls', is_admin=True)
    dp.register_callback_query_handler(otmena_admin, text='otmena_pls', state='*', is_admin=True)
    dp.register_callback_query_handler(panel_administrator, text='pokash_panel_admina', is_admin=True)
    dp.register_callback_query_handler(rassilka_waiting, text='rassilka_pls')
    dp.register_message_handler(rassilka_go, state='text_rassilki')
    dp.register_callback_query_handler(proverka_subscribe_admin, text='proverka_kanal', is_admin=True)
    dp.register_callback_query_handler(provekra_pay_admin, text_contains='check_', is_admin=True)
