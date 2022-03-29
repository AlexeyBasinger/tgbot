from aiogram import Dispatcher
from aiogram.types import CallbackQuery
from tgbot.config import db
from tgbot.keyboards.inline import menu, nasad


async def referal(call: CallbackQuery):
    await call.answer()
    await call.message.edit_text(f'Вы пригласили {await db.referalka1(call.from_user.id)} пользователей\n'
                                 f'Ваша скидка равна {await db.referalka2(call.from_user.id)} USD', reply_markup=nasad)


async def nasad_v_menu(call: CallbackQuery):
    await call.answer()
    await call.message.edit_text(f'🎉Поздравляю, вы получили доступ🎉\n'
                                 f'Вы можете получить 10 бонусных рублей за каждого преглашонного реферала!!!\n'
                                 f'Ваша реферальная ссылка: https://t.me/udemy_exam_bot?start={call.from_user.id}\n'
                                 f'Ваш код приглашения: {await db.priglos_id(call.from_user.id)}', reply_markup=menu)


async def proverka_bought_tovar(call: CallbackQuery):
    a = await db.prosmot_tovar_bought(call.from_user.id)
    result = 'Вы заказали:\n'
    if a:
        for b in a:
            result += f'{b[0]} в количестве: {b[1]}\n'
        await call.message.answer(result)
    else:
        await call.answer('Вы пока ничего не заказали', cache_time=5, show_alert=True)


def register_user(dp: Dispatcher):
    dp.register_callback_query_handler(referal, text='referal_open')
    dp.register_callback_query_handler(nasad_v_menu, text='nasad_pls')
    dp.register_callback_query_handler(proverka_bought_tovar, text='pokaz_tovar_bought')
