import json
import logging
import os

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Command
from aiogram.utils.exceptions import TelegramAPIError

from data.config import schedule_data_name, group_data_name
from keyboards.inline.callback_datas import day_callback, week_callback, schedule_callback
from keyboards.inline.choice_buttons import day_choice, week_choice, schedule_choice
from loader import dp
from states import ScheduleForm


# Формирование ответа
async def outputting(local_choice):
    global group_name
    tmp = ''
    answer = []
    try:
        with open(schedule_data_name) as json_file:
            data = json.load(json_file)
            if not data[group_name][local_choice]:
                return answer
            else:
                for i, subject in enumerate(data[group_name][local_choice]):
                    if len(subject) == 4:
                        answer.append(f'\n----------<u>{subject[0]}:</u>\n'
                                      '<b>Група:</b>\n'
                                      f'<b>Тип заняття</b>: {subject[3]}\n'
                                      f'<b>Предмет</b>: {subject[1]}\n'
                                      f'<b>Аудиторія:</b> {subject[2]}')
                    else:
                        if tmp == subject[0]:
                            answer[-1] += f'\n\n<b>Підгрупа {subject[2]}:</b>\n' \
                                          f'<b>Тип заняття</b>: {subject[4]}\n'\
                                          f'<b>Предмет</b>: {subject[1]}\n'\
                                          f'<b>Аудиторія:</b> {subject[3]}'
                        else:
                            answer.append(f'\n----------<u>{subject[0]}:</u>\n'
                                          f'<b>Підгрупа {subject[2]}:</b>\n'
                                          f'<b>Тип заняття</b>: {subject[4]}\n'
                                          f'<b>Предмет</b>: {subject[1]}\n'
                                          f'<b>Аудиторія:</b> {subject[3]}')
                        tmp = subject[0]
                answer.append('\n\n\nОтримати розклад - /schedule')
                return answer
    except KeyError:
        logging.error('User clicked a lot of times on a button')


@dp.message_handler(Command('schedule'))
async def schedule_enter(message: types.Message):
    global user_names_dict
    user_names_dict = {
        'full_name': message.from_user.full_name,
        'username': message.from_user.username
    }
    logging.info(f'Answering user: {message.from_user.full_name} (@{message.from_user.username})')

    if not os.path.exists(group_data_name):
        with open(group_data_name, 'w') as f:
            f.write('{}')
    
    with open(group_data_name) as json_file:
        data = json.load(json_file)
        try:
            d = data[str(message.from_user.id)]
        except KeyError:
            await message.answer('Введіть абревіатуру вашої групи(приклад: ІПЗ-20-4, іПз-20-4). '
                                 'Також у вас є можливість вказати групу за замовчуванням',
                                 reply_markup=schedule_choice)
            await ScheduleForm.GROUP_NAME.set()
        else:
            await ScheduleForm.GROUP_NAME.set()
            await group_input(message)


@dp.message_handler(state=ScheduleForm.GROUP_NAME)
async def group_input(message: types.Message):
    global group_name
    message.message_id -= 1
    try:
        await message.edit_reply_markup()
    except TelegramAPIError:
        pass
    message.message_id += 1
    with open(group_data_name) as json_file:
        data = json.load(json_file)
        try:
            d = data[str(message.from_user.id)]
        except KeyError:
            logging.info(f'From: {message.from_user.full_name} (@{message.from_user.username}) -> {message.text}')
            group_name = message.text.upper()
            # Проверка на правильное название группы
            try:
                with open(schedule_data_name) as json_file_inner:
                    d = json.load(json_file_inner)
                    d = d[group_name]
            except KeyError:
                await message.answer('Неправильно введена група. Спробуйте ще раз')
                return
        else:
            group_name = data[str(message.from_user.id)]

    await ScheduleForm.WEEK_DAY.set()
    await message.answer('Оберіть день тижня', reply_markup=day_choice)


@dp.callback_query_handler(day_callback.filter(), state=ScheduleForm.WEEK_DAY)
async def day_input(call: types.CallbackQuery, callback_data: dict):
    global choice
    await call.answer(cache_time=5)
    choice = callback_data.get('day_name')
    await call.message.edit_reply_markup()
    await ScheduleForm.WEEK_NUM.set()
    await call.message.answer('Оберіть номер тижня', reply_markup=week_choice)


@dp.message_handler(state=ScheduleForm.WEEK_DAY)
async def spam_while_need_day(message: types.Message):
    await message.answer('Будь ласка, не дратуйте мене і оберіть день тижня.')


@dp.callback_query_handler(week_callback.filter(), state=ScheduleForm.WEEK_NUM)
async def week_input(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    global choice, user_names_dict
    await call.answer(cache_time=5)
    choice += f' {callback_data.get("week_number")}'
    logging.info(f'{user_names_dict["full_name"]} (@{user_names_dict["username"]}) :::: chose day "{choice}"')
    answer = await outputting(choice)
    if answer == []:
        await call.message.answer('У цей день у вас немає пар, вітаю! :)')
    else:
        try:
            await call.message.answer('\n'.join(answer))
        except TypeError:
            pass
    await call.message.edit_reply_markup()
    await state.reset_state()


@dp.message_handler(state=ScheduleForm.WEEK_NUM)
async def spam_while_need_week(message: types.Message):
    await message.answer('Будь ласка, не дратуйте мене і оберіть номер тижня.')


@dp.callback_query_handler(schedule_callback.filter(cancel='true'), state=ScheduleForm.GROUP_NAME)
async def schedule_cancel(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    global user_names_dict
    await call.answer(cache_time=5)
    await call.message.delete()
    await call.message.answer('Ви відмінили операцію.')
    logging.info(f'{user_names_dict["full_name"]} (@{user_names_dict["username"]}) :::: canceled operation')
    await state.reset_state()


@dp.callback_query_handler(text='cancel_week', state=ScheduleForm.WEEK_DAY)
async def week_cancel(call: types.CallbackQuery, state: FSMContext):
    global user_names_dict
    await call.answer(cache_time=5)
    await call.message.delete()
    await call.message.answer('Ви відмінили операцію.')
    logging.info(f'{user_names_dict["full_name"]} (@{user_names_dict["username"]}) :::: canceled operation')
    await state.reset_state()
