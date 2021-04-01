import json
import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.exceptions import TelegramAPIError

from data.config import schedule_data_name, group_data_name
from keyboards.inline.callback_datas import group_edit_callback
from keyboards.inline.choice_buttons import group_edit_choice
from loader import dp
from states.group import GroupSave


@dp.message_handler(Command('group'))
async def edit_choose(message: types.Message):
    global user_names_dict
    user_names_dict = {
        'full_name': message.from_user.full_name,
        'username': message.from_user.username
    }
    await message.answer('Оберіть дію', reply_markup=group_edit_choice)


@dp.callback_query_handler(group_edit_callback.filter(group_edit_choice='add'))
async def group_save(call: types.CallbackQuery, callback_data: dict):
    await call.answer(cache_time=5)
    await call.message.answer('Введіть групу за замовчуванням',
                              reply_markup=InlineKeyboardMarkup(row_width=1,
                                                                inline_keyboard=[
                                                                    [
                                                                        InlineKeyboardButton(
                                                                            text='🔎Пошук',
                                                                            switch_inline_query_current_chat=''
                                                                        )
                                                                    ],
                                                                    [
                                                                        InlineKeyboardButton(
                                                                            text='🔴Відміна',
                                                                            callback_data=group_edit_callback.new('cancel')
                                                                        )
                                                                    ]
                                                                ]))
    await call.message.edit_reply_markup()
    await GroupSave.GROUP_SAVE.set()


@dp.callback_query_handler(group_edit_callback.filter(group_edit_choice='delete'))
async def group_delete(call: types.CallbackQuery, callback_data: dict):
    global user_names_dict
    await call.answer(cache_time=5)
    try:
        with open(group_data_name) as json_file:
            data = json.load(json_file)
            del data[f'{call.from_user.id}']
        with open(group_data_name, 'w') as json_file:
            json.dump(data, json_file, indent=4)

        logging.info(f'User {user_names_dict["full_name"]} (@{user_names_dict["username"]}) deleted his group')
        await call.message.edit_text('Група видалена')
    except KeyError:
        await call.message.answer('У вас не вказана група за замовчуванням')
    finally:
        await call.message.edit_reply_markup()


@dp.callback_query_handler(group_edit_callback.filter(group_edit_choice='cancel'))
@dp.callback_query_handler(group_edit_callback.filter(group_edit_choice='cancel'), state=GroupSave.GROUP_SAVE)
async def group_cancel(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=5)
    await call.message.delete()
    await call.message.answer('Ви відмінили операцію.')
    await state.reset_state()
    logging.info(f'{user_names_dict["full_name"]} (@{user_names_dict["username"]}) :::: canceled operation')


@dp.message_handler(state=GroupSave.GROUP_SAVE)
async def setting_group(message: types.Message, state: FSMContext):
    group = message.text.upper()
    message.message_id -= 1
    try:
        await message.edit_reply_markup()
    except TelegramAPIError:
        pass
    message.message_id += 1
    # Проверка на правильное название группы
    try:
        with open(schedule_data_name) as json_file:
            d = json.load(json_file)
            d = d[group]
    except KeyError:
        await message.answer('Неправильно введена група. Спробуйте ще раз')
        return

    try:
        data = {}
        with open(group_data_name) as json_file:
            data = json.load(json_file)
            data[message.from_user.id] = group
        with open(group_data_name, "w") as json_file:
            json.dump(data, json_file, indent=4)
    except FileNotFoundError:
        with open(group_data_name, "w") as json_file:
            data[message.from_user.id] = group
            json.dump(data, json_file, indent=4)

    logging.info(f'User {message.from_user.full_name} (@{message.from_user.username}) saved his group')
    await message.answer('Група збережена')
    await state.reset_state()
