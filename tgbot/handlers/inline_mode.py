from aiogram import Dispatcher
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardMarkup, \
    InlineKeyboardButton
from tgbot.payment.QIWI import db


async def inline_katalog(query: InlineQuery):
    if await db.poluchit_id_inline_mod(query.from_user.id):
        if query.query == '':
            lits_tovarov = await db.pol_vse()
        else:
            lits_tovarov = await db.select_name(f'{query.query}%')
        tovari = [InlineQueryResultArticle(
            id=a[0],
            title=a[2],
            input_message_content=InputTextMessageContent(message_text=f'название: <b>{a[2]}</b>\n'
                                                                       f'Описание: <b>{a[3]}</b>\n'
                                                                       f'Цена: <b>{a[4]}</b> Руб.', parse_mode='HTML'),
            description=f'{a[4]} Руб.',
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
                text='Показать товар', url=f'https://t.me/udemy_exam_bot?start={a[0]}')]])
        ) for a in lits_tovarov]
        if tovari:
            await query.answer(tovari)
        else:
            await query.answer(results=[], switch_pm_text='Товары в базе данных отсутствуют'
                               , switch_pm_parameter='qwertyqw')
    else:
        await query.answer(results=[], switch_pm_text='Бот недоступен, вы должны войти в него!'
                           , switch_pm_parameter='qwerty')


def register_inline_mode_handlers(dp: Dispatcher):
    dp.register_inline_handler(inline_katalog)
