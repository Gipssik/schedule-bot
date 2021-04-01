from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp
from utils.misc import rate_limit


@rate_limit(5, 'help')
@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = [
        'Список команд: ',
        '/start - Розпочати діалог',
        '/help - Отримати справку',
        '/schedule - Дізнатися розклад',
        '/group - Встановити/Змінити/Видалити групу за замовчуванням'
    ]
    await message.answer('\n'.join(text))
