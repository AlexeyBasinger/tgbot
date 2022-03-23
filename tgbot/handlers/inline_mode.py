from aiogram import Dispatcher
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardMarkup, \
    InlineKeyboardButton

from tgbot.config import db


async def inline_katalog(query: InlineQuery):
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
    await query.answer(tovari)


def register_inline_mode_handlers(dp: Dispatcher):
    dp.register_inline_handler(inline_katalog)
