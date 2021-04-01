import logging

import aiogram
from aiogram import types
from loader import dp, bot


@dp.message_handler()
async def bot_spam(message: types.Message):
    logging.info(f'From: {message.from_user.full_name} (@{message.from_user.username}) -> {message.text}')
    await message.answer('Натисніть /schedule для отримання розкладу.')
