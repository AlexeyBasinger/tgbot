from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message, ContentType
from tgbot.payment.QIWI import db
from tgbot.db_api.FSM import tovar
from tgbot.keyboards.inline import cancel_inline_button, menu, potverdit_tovar, menu_admin


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
    if len(message.text) > 255:
        await message.answer('Описание слишком длинное!\n'
                             'Максимальная длинна 255 символов!')
    else:
        async with state.proxy() as data:
            data['description'] = message.text
        await tovar.next()
        await message.answer('введите цену товара', reply_markup=cancel_inline_button)


async def tovar_price(message: Message, state: FSMContext):
    try:
        if int(message.text) >= 60000:
            async with state.proxy() as data:
                data['price'] = int(message.text)
                await tovar.next()
                await message.answer('введите количество товара', reply_markup=cancel_inline_button)
        else:
            await message.answer('Максимально возможная цена 60000')
    except ValueError:
        await message.answer('Пришли цену без посторонних символов')


async def tovar_amount(message: Message, state: FSMContext):
    try:
        if int(message.text) < 2147483647:
            async with state.proxy() as data:
                data['amount'] = int(message.text)
            await tovar.next()
            await message.answer('введите артикул', reply_markup=cancel_inline_button)
        else:
            await message.answer('Слишком большое значение')
    except ValueError:
        await message.answer('Введите только число!')


async def tovar_articul(message: Message, state: FSMContext):
    try:
        if int(message.text) < 2147483647:
            async with state.proxy() as data:
                data['articul'] = int(message.text)
            data = await state.get_data()
            await message.bot.send_photo(chat_id=message.chat.id, photo=data.get('photo'),
                                         caption=f'аритикул: <b>{data.get("articul")}</b>\n'
                                                 f'название: <b>{data.get("name")}</b>\n'
                                                 f'количество: <b>{data.get("amount")}</b>\n'
                                                 f'Описание: <b>{data.get("description")}</b>\n'
                                                 f'Цена: <b>{data.get("price")}</b> Руб.',
                                         parse_mode='HTML', reply_markup=potverdit_tovar)
        else:
            await message.answer('слишком большое значение!')
    except ValueError:
        await message.answer('Введите только число(номер артикула)!')


async def dobavit_tovar_pop(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await db.add_tovar(img=data.get('photo'), name=data.get('name'), description=data.get('description'),
                       price=data.get('price'), amount=data.get('amount'), articul=data.get('articul'))
    await state.finish()
    await call.message.delete()
    await call.message.answer('Товар добавлен', reply_markup=menu_admin)
    await call.answer()


async def udalit_tovar(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.set_state('udoli_art')
    await call.message.delete()
    await call.message.answer('Введите артикул товара которого вы хотите удалить ',
                              reply_markup=cancel_inline_button)


async def udalyu(message: Message, state: FSMContext):
    try:
        if await db.right_udoli(int(message.text)):
            await db.udoli_pls(int(message.text))
            await message.answer('Удалено', reply_markup=menu_admin)
            await state.finish()
        else:
            await message.answer('Такого артикула нету в базе данных')
    except ValueError:
        await message.answer('Введите только число(номер артикула)!')


async def otmena(call: CallbackQuery, state=FSMContext):
    cur_state = await state.get_state()
    if cur_state is None:
        return
    await state.finish()
    await call.message.delete()
    await call.message.answer('Операция была отменена', reply_markup=menu)
    await call.answer()


async def sanovo_vse(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.delete()
    await tovar.img.set()
    await call.message.answer('Пришли фото товара!!!', reply_markup=cancel_inline_button)


def register_insert_delete_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(dobavit_t, text='dobavit_tovar')
    dp.register_message_handler(tovar_photo, content_types=ContentType.PHOTO, state=tovar.img)
    dp.register_message_handler(tovar_name, state=tovar.name)
    dp.register_message_handler(tovar_description, state=tovar.description)
    dp.register_message_handler(tovar_price, state=tovar.price)
    dp.register_message_handler(tovar_amount, state=tovar.amount)
    dp.register_message_handler(tovar_articul, state=tovar.articul)
    dp.register_callback_query_handler(dobavit_tovar_pop, text='confirm_tovar_srochno', state=tovar.articul)
    dp.register_callback_query_handler(sanovo_vse, text='davai_po_novoi', state=tovar.articul)
    dp.register_callback_query_handler(udalit_tovar, text='udalit_tovar')
    dp.register_message_handler(udalyu, state='udoli_art')
    dp.register_callback_query_handler(otmena, text='otmena_pls', state='*')
