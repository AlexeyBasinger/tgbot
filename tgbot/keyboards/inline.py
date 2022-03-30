from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

code = InlineKeyboardMarkup(row_width=1)
test = InlineKeyboardButton(text='✏️Код приглашения✏️', callback_data='code_text')
canal_sub = InlineKeyboardButton(text='Проверить подписку на канал', callback_data='proverka_kanal')
code.insert(test)
code.insert(canal_sub)



menu = InlineKeyboardMarkup(row_width=2)
katalog = InlineKeyboardButton(text='🛒Каталог', switch_inline_query_current_chat='')
referals = InlineKeyboardButton(text='🌐Рефералка', callback_data='referal_open')
pop_pop = InlineKeyboardButton(text='Оплаченные заказы', callback_data='pokaz_tovar_bought')
menu.insert(katalog)
menu.insert(referals)
menu.insert(pop_pop)



menu_admin = InlineKeyboardMarkup(row_width=2)
panel_admin = InlineKeyboardButton(text='🎛Панель админа', callback_data='pokash_panel_admina')
menu_admin.insert(katalog)
menu_admin.insert(referals)
menu_admin.insert(pop_pop)
menu_admin.insert(panel_admin)




nasad = InlineKeyboardMarkup()
nasad_menu = InlineKeyboardButton(text='🔙Назад', callback_data='nasad_pls')
nasad.insert(nasad_menu)



menu_admina_2 = InlineKeyboardMarkup(row_width=2)
rassilka_admin = InlineKeyboardButton(text='📢Рассылка', callback_data='rassilka_pls')
insert = InlineKeyboardButton(text='🎁Добавить товар', callback_data='dobavit_tovar')
udalit = InlineKeyboardButton(text='✂️Удалить товар', callback_data='udalit_tovar')
menu_admina_2.insert(insert)
menu_admina_2.insert(udalit)
menu_admina_2.insert(rassilka_admin)
menu_admina_2.insert(nasad_menu)



cancel_inline_button = InlineKeyboardMarkup()
cancel_button = InlineKeyboardButton(text='❌Отмена', callback_data='otmena_pls')
cancel_inline_button.insert(cancel_button)


potverdit_tovar = InlineKeyboardMarkup(row_width=1)
da_potverdit = InlineKeyboardButton(text='Добавить товар', callback_data='confirm_tovar_srochno')
sanovo = InlineKeyboardButton(text='Ввести все заново', callback_data='davai_po_novoi')
potverdit_tovar.insert(da_potverdit)
potverdit_tovar.insert(sanovo)
potverdit_tovar.insert(cancel_button)