from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup

inline_payments = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='🟢 1 МЕС • 2000₽ • 30 дней',callback_data='buy_30')],
                                                        [InlineKeyboardButton(text='🟡 3 МЕС • 5400₽ • -10% • 90 дней',callback_data='buy_90')],
                                                        [InlineKeyboardButton(text='🔴 1 ГОД • 18000₽ • -25% • 365 дней',callback_data='buy_365')],
                                                        [InlineKeyboardButton(text="🔙 Назад", callback_data="nazads")]])
inline_buy = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='💳 Оплатить',callback_data='payment')],
                                                #    [InlineKeyboardButton(text='🎁 Применить промокод',callback_data='promo')],
                                                   [InlineKeyboardButton(text='🔙 Назад',callback_data='nazad')]])
inline_op = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='💳 ЮKassa (карты РФ)',callback_data='yookas')],
                                                  [InlineKeyboardButton(text='₿ CryptoBot (крипта)',callback_data='crypto')],
                                                  [InlineKeyboardButton(text="🔙 Назад", callback_data="nazad")]])
inline_otm = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Отмена',callback_data='canel')]])
# inline_bu = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Перейти к оплате 💰',url=invoice.pay_url)],
#                                                   [InlineKeyboardButton(text="🔙 Назад", callback_data="nazad")]])

inline_payments_club = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='🟢 1 МЕС • 10 000₽ • 30 дней',callback_data='buy:30')],
                                                        [InlineKeyboardButton(text='🟡 3 МЕС • 27 000₽ • -10% • 90 дней',callback_data='buy:90')],
                                                        [InlineKeyboardButton(text='🔴 1 ГОД • 90 000₽ • -25% • 365 дней',callback_data='buy:365')],
                                                        [InlineKeyboardButton(text="🔙 Назад", callback_data="nazads")]])

