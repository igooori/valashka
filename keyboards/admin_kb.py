from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup


keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👥 Все пользователи", callback_data="admin_users")],
        [InlineKeyboardButton(text="💰 Платежи", callback_data="admin_payments")],
        [InlineKeyboardButton(text="📊 Статистика", callback_data="admin_stats")]
    ])
reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📋 Список пользователей", callback_data="users_list")],
            [InlineKeyboardButton(text="◀️ Назад", callback_data="admin_back")]
        ])
reply_markap=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📋 Список платежей", callback_data="payments_list")],
            [InlineKeyboardButton(text="⏳ Ожидающие платежи", callback_data="pending_payments")],
            [InlineKeyboardButton(text="◀️ Назад", callback_data="admin_back")]
        ])
reply_nazad=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="◀️ Назад", callback_data="admin_back")]
        ])