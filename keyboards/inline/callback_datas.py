from aiogram.utils.callback_data import CallbackData

schedule_callback = CallbackData('schedule_cancel', 'cancel')
day_callback = CallbackData('day_choose', 'day_name')
week_callback = CallbackData('week_choose', 'week_number')
group_edit_callback = CallbackData('group_edit', 'group_edit_choice')
