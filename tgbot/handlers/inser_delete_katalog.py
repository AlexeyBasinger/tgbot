from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message, ContentType

from tgbot.config import db
from tgbot.db_api.FSM import tovar
from tgbot.keyboards.inline import cancel_inline_button, menu


async def dobavit_t(call: CallbackQuery):
    await call.answer()
    await call.message.delete()
    await tovar.img.set()
    await call.message.answer('Пришли фото товара!!!', reply_markup=cancel_inline_button)


async def tovar_photo(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[-1].file_id
    await tovar.next()
    await message.answer('введите име товара', reply_markup=cancel_inline_button)


async def tovar_name(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await tovar.next()
    await message.answer('введите описание', reply_markup=cancel_inline_button)


async def tovar_description(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
    await tovar.next()
    await message.answer('введите цену товара', reply_markup=cancel_inline_button)


async def tovar_price(message: Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['price'] = int(message.text)
            await tovar.next()
            await message.answer('введите количество товара', reply_markup=cancel_inline_button)
    except ValueError:
        await message.answer('Пришли цену без посторонних символов')


async def tovar_amount(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['amount'] = int(message.text)
    await tovar.next()
    await message.answer('введите артикул', reply_markup=cancel_inline_button)


async def tovar_articul(message: Message, state: FSMContext):
    data = await state.get_data()
    await db.add_tovar(img=data.get('photo'), name=data.get('name'), description=data.get('description'),
                       price=data.get('price'), amount=data.get('amount'), articul=int(message.text))
    await state.finish()
    await message.answer('Товар добавлен', reply_markup=menu)


async def udalit_tovar(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.set_state('udoli_art')
    await call.message.delete()
    await call.message.answer('Введите артикул товара которого вы хотите удалить ',
                              reply_markup=cancel_inline_button)


async def udalyu(message: Message, state: FSMContext):
    await db.udoli_pls(int(message.text))
    await message.answer('Удалено', reply_markup=menu)
    await state.finish()


async def otmena(call: CallbackQuery, state=FSMContext):
    cur_state = await state.get_state()
    if cur_state is None:
        return
    await state.finish()
    await call.message.edit_text('Операция была отменена', reply_markup=menu)
    await call.answer()


def register_insert_delete_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(dobavit_t, text='dobavit_tovar')
    dp.register_message_handler(tovar_photo, content_types=ContentType.PHOTO, state=tovar.img)
    dp.register_message_handler(tovar_name, state=tovar.name)
    dp.register_message_handler(tovar_description, state=tovar.description)
    dp.register_message_handler(tovar_price, state=tovar.price)
    dp.register_message_handler(tovar_amount, state=tovar.amount)
    dp.register_message_handler(tovar_articul, state=tovar.articul)
    dp.register_callback_query_handler(udalit_tovar, text='udalit_tovar')
    dp.register_message_handler(udalyu, state='udoli_art')
    dp.register_callback_query_handler(otmena, text='otmena_pls', state='*')
