import re
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncpg
from aiogram import Dispatcher
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.utils.markdown import hcode
from tgbot.config import db
from tgbot.keyboards.inline import menu, code


async def user_start(message: Message):
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
                             f'Вы можете получить 10 бонусных доларов за каждого приглашенного реферала!!!\n'
                             f'Ваша реферальная ссылка: https://t.me/udemy_exam_bot?start={message.from_user.id}\n'
                             f'Ваш код приглашения: {await db.priglos_id(telegram_id=message.from_user.id)}\n',
                             reply_markup=menu)




    else:
        await message.answer('❌Ошибка❌\n'
                             '🔒У вас нет доступа!!!\n'
                             'Чтобы использывать бота введите код приглашения,\n'
                             'либо пройдите по реферальной ссылке\n'
                             f'Если вас никто не пригласил, то просто подпишись на данный канал: https://t.me/testUdemyCors\n'
                             f'Затем нажми на кнопку проверить подписку', reply_markup=code)


async def start_netdipa(message: Message):
    user_id = int(message.from_user.id)
    if await db.poluchit_poshalusta_id_true(user_id):
        await message.answer(f'Поздравляю, вы получили доступ🎉\n'
                             f'Вы можете получить 10 бонусных доларов за каждого приглашенного реферала!!!\n'
                             f'Ваша реферальная ссылка: https://t.me/udemy_exam_bot?start={user_id}\n'
                             f'Ваш код приглашения: {await db.priglos_id(telegram_id=user_id)}\n',
                             reply_markup=menu)
    else:
        await message.answer('❌Ошибка❌\n'
                             '🔒У вас нет доступа!!!\n'
                             'Чтобы использывать бота введите код приглашения,\n'
                             'либо пройдите по реферальной ссылке\n'
                             f'Если вас никто не пригласил, то просто подпишись на данный канал: https://t.me/testUdemyCors\n'
                             f'Затем нажми на кнопку проверить подписку', reply_markup=code)


async def tovar_pokaz(message: Message):
    args = message.get_args()
    a = await db.poluchit_vse_deep_link(int(args))
    if args in hcode(await db.pokasi_id()):
        await message.bot.send_photo(chat_id=message.chat.id, photo=a[1],
                                     caption=f'аритикул: <b>{a[-1]}</b>\n'
                                             f'название: <b>{a[2]}</b>\n'
                                             f'количество: <b>{a[-2]}</b>\n'
                                             f'Описание: <b>{a[3]}</b>\n'
                                             f'Цена: <b>{a[4]}</b> Руб.',
                                     parse_mode='HTML',
                                     reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='💰Купить товар', callback_data=f'buy_tovar_{a[0]}')]]))
    else:
        await message.answer('❌Ошибка❌\n'
                             '🔒У вас нет доступа!!!\n'
                             'Чтобы использывать бота введите код приглашения,\n'
                             'либо пройдите по реферальной ссылке\n'
                             f'Если вас никто не пригласил, то просто подпишись на данный канал: https://t.me/testUdemyCors\n'
                             f'Затем нажми на кнопку проверить подписку', reply_markup=code)


async def proverka_subscribe(call: CallbackQuery):
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
                                     reply_markup=menu)
    else:
        await call.message.answer('❌Ошибка❌\n'
                                  '🔒У вас нет доступа!!!\n'
                                  'Чтобы использывать бота введите код приглашения,\n'
                                  'либо пройдите по реферальной ссылке\n'
                                  f'Если вас никто не пригласил, то просто подпишись на данный канал: https://t.me/testUdemyCors\n'
                                  f'Затем нажми на кнопку проверить подписку', reply_markup=code)


def register_start_handlers(dp: Dispatcher):
    dp.register_message_handler(tovar_pokaz, CommandStart(deep_link=re.compile(r'^[0-9]{1,3}$')))
    dp.register_message_handler(user_start, CommandStart(deep_link=re.compile(r"^[0-9]{4,15}$")))
    dp.register_message_handler(start_netdipa, CommandStart())
    dp.register_callback_query_handler(proverka_subscribe, text='proverka_kanal')
