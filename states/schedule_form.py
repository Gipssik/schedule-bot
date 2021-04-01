from aiogram.dispatcher.filters.state import StatesGroup, State


class ScheduleForm(StatesGroup):
    GROUP_NAME = State()
    WEEK_DAY = State()
    WEEK_NUM = State()
