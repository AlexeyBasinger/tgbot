import asyncpg
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.markdown import hcode
from tgbot.payment.QIWI import db
from tgbot.keyboards.inline import code, menu


async def code_invite(call: CallbackQuery, state: FSMContext):
    await state.set_state('code')
    await call.message.edit_text('Пришли мне код')


async def wait_code(message: Message, state: FSMContext):
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
                             'Вы можете получить 1 бонусный долар за каждого преглашонного реферала!!!\n'
                             f'Ваша реферальная ссылка: https://t.me/udemy_exam_bot?start={message.from_user.id}\n'
                             f'Ваш код приглашения: {await db.priglos_id(message.from_user.id)}', reply_markup=menu)


    else:
        await message.answer('❌Ошибка❌\n'
                             '🔒У вас нет доступа!!!\n'
                             'Чтобы использывать бота введите код приглашения,\n'
                             'либо пройдите по реферальной ссылке\n'
                             f'Если вас никто не пригласил, то просто подпишись на данный канал: https://t.me/testUdemyCors\n'
                             f'Затем нажми на кнопку проверить подписку', reply_markup=code)
    await state.finish()


def register_code(dp: Dispatcher):
    dp.register_callback_query_handler(code_invite, text='code_text')
    dp.register_message_handler(wait_code, state='code')
