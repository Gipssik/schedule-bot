from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    text = [
        f'Привіт, {message.from_user.full_name}!',
        'Список команд: ',
        '/help - Отримати справку',
        '/schedule - Дізнатися розклад',
        '/group - Встановити/Змінити/Видалити групу за замовчуванням'
    ]
    await message.answer('\n'.join(text))
