from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import day_callback, week_callback, group_edit_callback, schedule_callback

schedule_choice = InlineKeyboardMarkup(row_width=1,
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
                                                   callback_data=schedule_callback.new('true')
                                               ),
                                           ]
                                       ])

day_choice = InlineKeyboardMarkup(row_width=2,
                                  inline_keyboard=[
                                      [
                                          InlineKeyboardButton(
                                              text='Понеділок',
                                              callback_data=day_callback.new('Понеділок')
                                          ),
                                          InlineKeyboardButton(
                                              text='Вівторок',
                                              callback_data=day_callback.new('Вівторок')
                                          )
                                      ],
                                      [
                                          InlineKeyboardButton(
                                              text='Середа',
                                              callback_data=day_callback.new('Середа')
                                          ),
                                          InlineKeyboardButton(
                                              text='Четвер',
                                              callback_data=day_callback.new('Четвер')
                                          )
                                      ],
                                      [
                                          InlineKeyboardButton(
                                              text="П'ятниця",
                                              callback_data=day_callback.new("П'ятниця")
                                          )
                                      ],
                                      [
                                          InlineKeyboardButton(
                                              text='🔴Відміна',
                                              callback_data='cancel_week'
                                          )
                                      ]
                                  ])

week_choice = InlineKeyboardMarkup(row_width=2,
                                   inline_keyboard=[
                                       [
                                           InlineKeyboardButton(
                                               text='1️⃣',
                                               callback_data=week_callback.new(1)
                                           ),
                                           InlineKeyboardButton(
                                               text='2️⃣',
                                               callback_data=week_callback.new(2)
                                           )
                                       ]
                                   ])

group_edit_choice = InlineKeyboardMarkup(row_width=2,
                                         inline_keyboard=[
                                             [
                                                 InlineKeyboardButton(
                                                     text='📁Встановити/Змінити',
                                                     callback_data=group_edit_callback.new('add')
                                                 ),
                                                 InlineKeyboardButton(
                                                     text='❌Видалити',
                                                     callback_data=group_edit_callback.new('delete')
                                                 )
                                             ],
                                             [
                                                 InlineKeyboardButton(
                                                     text='🔴Відміна',
                                                     callback_data=group_edit_callback.new('cancel')
                                                 ),
                                             ]
                                         ])
