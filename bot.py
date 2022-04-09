import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from tgbot.config import load_config
from tgbot.config import db
from tgbot.filters.admin import AdminFilter
from tgbot.handlers.Start_handlers import register_start_handlers
from tgbot.handlers.admin import register_admin
from tgbot.handlers.code_request import register_code
from tgbot.handlers.dostavka__opata import register_all_oplata_handlers
from tgbot.handlers.inline_mode import register_inline_mode_handlers
from tgbot.handlers.inser_delete_katalog import register_insert_delete_handlers
from tgbot.handlers.user import register_user
from tgbot.integrations.telegraph.abstract import FileUploader
from tgbot.integrations.telegraph.client import Telegraph
from tgbot.middlewares.integration import IntegrationMiddleware
from tgbot.middlewares.throttling import ThrottlingMiddleware

logger = logging.getLogger(__name__)


async def on_shutdown(dp: Dispatcher):
    file_uploader: FileUploader = dp.bot["file_uploader"]
    await file_uploader.close()


def register_all_middlewares(dp):
    dp.middleware.setup(ThrottlingMiddleware())


def register_all_filters(dp):
    dp.filters_factory.bind(AdminFilter)


def register_all_handlers(dp):
    register_admin(dp)
    register_start_handlers(dp)
    register_user(dp)
    register_code(dp)
    register_insert_delete_handlers(dp)
    register_inline_mode_handlers(dp)
    register_all_oplata_handlers(dp)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")
    config = load_config(".env")

    storage = RedisStorage2() if config.tg_bot.use_redis else MemoryStorage()
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    file_uploader = Telegraph()
    dp = Dispatcher(bot, storage=storage)
    dp.middleware.setup(IntegrationMiddleware(file_uploader))

    bot['file_uploader'] = file_uploader
    bot['config'] = config

    register_all_middlewares(dp)
    register_all_filters(dp)
    register_all_handlers(dp)
    await db.create()
    await db.create_table_users_referal()
    await db.create_table_tovar()
    await db.create_table_tovar_oplata()

    # start
    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()
        await on_shutdown(dp)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
