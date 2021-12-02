import logging

from aiogram import Dispatcher

from data.config import Config


async def on_startup_notify(dp: Dispatcher):
    for admin in Config.get_admins():
        try:
            await dp.bot.send_message(admin, "Bot started")

        except Exception as err:
            logging.exception(err)
