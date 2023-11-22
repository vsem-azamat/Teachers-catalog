import logging
import asyncio
from aiogram import Bot, Dispatcher

from bot.handlers import main_router
from bot.config import settings


async def on_startup(bot: Bot) -> None:
    await bot.delete_webhook()


async def on_shutdown(bot: Bot) -> None:
    await bot.delete_webhook()
    await bot.session.close()


# Run bot
async def main() -> None:
    bot = Bot(token=settings.BOT_TOKEN, parse_mode="HTML")
    dp = Dispatcher()
    
    try:
        dp.include_router(main_router)
        dp.startup.register(on_startup)
        dp.shutdown.register(on_shutdown)
        await dp.start_polling(bot, skip_updates=True)

    except Exception as e:
        logging.info(e)

    finally:
        await bot.session.close()



if __name__ == "__main__":
    asyncio.run(main())
