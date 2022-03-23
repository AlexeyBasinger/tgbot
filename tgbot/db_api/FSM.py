from aiogram.dispatcher.filters.state import StatesGroup, State


class tovar(StatesGroup):
    img = State()
    name = State()
    description = State()
    price = State()
    amount = State()
    articul = State()


class oplata_ru(StatesGroup):
    amount = State()
    street = State()
