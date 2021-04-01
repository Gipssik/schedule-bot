import re

from aiogram import types
from aiogram.utils.exceptions import TelegramAPIError

from data.config import schedule_data_name, group_names_name
from loader import dp
from states import ScheduleForm
from states.group import GroupSave


@dp.inline_handler(state=ScheduleForm.GROUP_NAME)
@dp.inline_handler(state=GroupSave.GROUP_SAVE)
async def group(query: types.InlineQuery):
    t = query.query.upper()
    with open(group_names_name) as txt_file:
        data = txt_file.read()
    try:
        await query.answer(
            results=[
                types.InlineQueryResultArticle(
                    id=str(i),
                    title=v,
                    input_message_content=types.InputTextMessageContent(
                        message_text=v
                    )
                ) for i, v in enumerate(data.split(',')) if t != '' and t in v
            ],
            cache_time=5,
        )
    except TelegramAPIError:
        pass
