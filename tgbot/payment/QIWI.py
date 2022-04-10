from pyqiwip2p import QiwiP2P

from tgbot.config import load_config
from tgbot.db_api.postgreSQL import Database

config = load_config(".env")
p2p = QiwiP2P(auth_key=config.qiwi.secret_token)
db = Database()
# async def oplata(message: Message):
#     comment = message.from_user.id
#     bill = p2p.bill(amount=5, lifetime=10, comment=comment)
#     await message.answer(bill.pay_url)
#     bill.bill_id
#
#
# check_ + bill
# @dp.message_hendler(text_contains='check_')
# async def check(call: CallbackQuery):
#     bill = call.data[6:]
#
# if str(p2p.check(bill_id=bill).status) == 'PAID':