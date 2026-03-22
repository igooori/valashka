from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup,KeyboardButton,ReplyKeyboardMarkup

main_inline = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Вступить в Путь',callback_data='subscraption')],
                                                    [InlineKeyboardButton(text=' Вступить в Силу ',callback_data='clube')],
                                                    [InlineKeyboardButton(text='Узнать про уровни', callback_data='levels_info')],
                                                    [InlineKeyboardButton(text='💬 Поддержка',callback_data='support')]])
main_inline2 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Вступить в Путь',callback_data='subscraption')],
                                                    [InlineKeyboardButton(text=' Вступить в Силу ',callback_data='clube')]])




