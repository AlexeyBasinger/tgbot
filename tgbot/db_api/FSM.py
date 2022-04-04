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


class price(StatesGroup):
    articul = State()
    price = State()


class amount(StatesGroup):
    articul = State()
    amount = State()
