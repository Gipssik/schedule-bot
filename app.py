import asyncio
from contextlib import suppress


async def call_parse():
    from utils.parse import parse
    while True:
        await parse()
        await asyncio.sleep(3600)


async def on_startup(dp):
    import filters
    import middlewares
    filters.setup(dp)
    middlewares.setup(dp)

    from utils.notify_admins import on_startup_notify
    task = asyncio.create_task(call_parse())


if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, on_startup=on_startup)
