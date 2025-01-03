import asyncio
import logging

import betterlogging as bl
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

from tgbot.config import load_config, Config
from tgbot.handlers import routers_list
from tgbot.middlewares.config import ConfigMiddleware
from tgbot.services import broadcaster


async def on_startup(bot: Bot, admin_ids: list[str | int]):
    await broadcaster.broadcast(bot, admin_ids, "Бот запущено!")


def register_global_middlewares(dp: Dispatcher, config: Config, session_pool=None):
    """
    Register global middlewares for the given dispatcher.
    Global middlewares here are the ones that are applied to all the handlers (you specify the type of update)

    :param dp: The dispatcher instance.
    :type dp: Dispatcher
    :param config: The configuration object from the loaded configuration.
    :param session_pool: Optional session pool object for the database using SQLAlchemy.
    :return: None
    """
    middleware_types = [
        ConfigMiddleware(config),
        # DatabaseMiddleware(session_pool),
    ]

    for middleware_type in middleware_types:
        dp.message.outer_middleware(middleware_type)
        dp.callback_query.outer_middleware(middleware_type)


def setup_logging():
    """
    Set up logging configuration for the application.

    This method initializes the logging configuration for the application.
    It sets the log level to INFO and configures a basic colorized log for
    output. The log format includes the filename, line number, log level,
    timestamp, logger name, and log message.

    Returns:
        None

    Example usage:
        setup_logging()
    """
    log_level = logging.INFO
    bl.basic_colorized_config(level=log_level)

    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s",
    )
    logger = logging.getLogger(__name__)
    logger.info("Starting bot")


def get_storage(config):
    """
    Return storage based on the provided configuration.

    Args:
        config (Config): The configuration object.

    Returns:
        Storage: The storage object based on the configuration.

    """
    if config.tg_bot.use_redis:
        return RedisStorage.from_url(
            config.redis.dsn(),
            key_builder=DefaultKeyBuilder(with_bot_id=True, with_destiny=True),
        )
    else:
        return MemoryStorage()


# async def main():
#     setup_logging()
#
#     config = load_config(".env")
#     storage = get_storage(config)
#
#     bot = Bot(token=config.tg_bot.token)
#     dp = Dispatcher(storage=storage)
#
#     dp.include_routers(*routers_list)
#
#     register_global_middlewares(dp, config)
#
#     await on_startup(bot, config.tg_bot.admin_ids)
#     await dp.start_polling(bot)
async def main():
    setup_logging()

    config = load_config(".env")
    storage = get_storage(config)

    # Initialize bot and dispatcher
    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher(storage=storage)

    dp.include_routers(*routers_list)
    register_global_middlewares(dp, config)

    # Create aiohttp web application
    app = web.Application()

    # Create a webhook handler
    webhook_handler = SimpleRequestHandler(
        dispatcher=dp, bot=bot, secret_token="your_secret_token"
    )

    # Set up the webhook handler
    webhook_handler.register(app, path="/bot")

    # Set up aiohttp routes
    setup_application(app, dp, bot=bot)

    # Set webhook URL
    await bot.set_webhook(
        url="https://bot.khamraev.uz/bot",
        secret_token="your_secret_token",
        drop_pending_updates=True,
    )

    # Start up notification
    await on_startup(bot, config.tg_bot.admin_ids)

    return app, bot, dp


def main_webhook():
    # Create application
    logging.basicConfig(level=logging.INFO)

    # Create new event loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # Create app and run startup
    app, bot, dp = loop.run_until_complete(main())

    # Setup web routes
    web.run_app(app, host="localhost", port=8080, loop=loop)


if __name__ == "__main__":
    main_webhook()
