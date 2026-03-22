from aiogram import Router,F
from aiogram.types import Message,CallbackQuery
from aiogram.filters import Command
from sqlalchemy.orm import Session
from models.user import User,Payment,engine
from settings import ADMIN_ID
from keyboards.admin_kb import keyboard,reply_markup,reply_markap,reply_nazad
from datetime import datetime

router = Router()

def is_admin(user_id:int) -> bool:
    return user_id in ADMIN_ID
@router.message(Command('admin'))
async def admin_panel(message:Message):
    if not is_admin(message.from_user.id):
        return
    await message.answer('🛠️ Админ-панель:',reply_markup=keyboard)
@router.callback_query(F.data == 'admin_users')
async def admin_users(callback:CallbackQuery):
    if not is_admin(callback.from_user.id):
        return
    with Session(bind=engine) as db:
        user_count = db.query(User).count()
        avtive_subs = db.query(User).filter(User.subscription_end > datetime.now()).count()
        await callback.message.edit_text(
            f"👥 Пользователи:\n"
        f"• Всего: {user_count}\n"
        f"• Активных подписок: {avtive_subs}\n\n"
        f"Выберите действие:",
        reply_markup=reply_markup
        )
@router.callback_query(F.data == 'admin_payments')
async def admin_payments(callback:CallbackQuery):
    if not is_admin(callback.from_user.id):
        return
    with Session(bind=engine) as db:
        total_payments = db.query(Payment).count()
        pending_payments = db.query(Payment).filter_by(status='pending').count()
        paid_payments = db.query(Payment).filter_by(status='paid').count()
    await callback.message.edit_text(
        f"💰 Платежи:\n"
        f"• Всего: {total_payments}\n"
        f"• Ожидают: {pending_payments}\n"
        f"• Оплачено: {paid_payments}\n\n"
        f"Выберите действие:",reply_markup=reply_markap
    )
@router.callback_query(F.data == 'admin_stats')
async def admin_stats(callback:CallbackQuery):
    if not is_admin(callback.from_user.id):
        return
    with Session(bind=engine) as db:
        total_income = db.query(Payment).filter_by(status='paid')
        total_rub = sum(p.amount_rub for p in total_income if p.amount_rub)
        total_usdt = sum(p.amount_usdt for p in total_income if p.amount_usdt)
        subscription = db.query(Payment).filter_by(product_type='subscription',status='paid').count()
        club = db.query(Payment).filter_by(product_type='club',status='paid').count()
        await callback.message.edit_text(
            f"📊 Статистика:\n\n"
        f"💰 Доходы:\n"
        f"• RUB: {total_rub:.2f}₽\n"
        f"• USDT: {total_usdt:.2f}\n\n"
        f"🎯 Популярность:\n"
        f"• Подписки: {subscription}\n"
        f"• Клуб: {club}\n",
        reply_markup=reply_nazad
        )
@router.callback_query(F.data == 'payments_list')
async def payments_list(callback:CallbackQuery):
    if not is_admin(callback.from_user.id):
        return
    with Session(bind=engine) as db:
        payments = db.query(Payment).order_by(Payment.created_at.desc()).limit(10).all()
        text = '📋 Последние 10 платежей:\n\n'
        for payment in payments:
            text += f'• {payment.user_id} - {payment.amount_rub}₽ - {payment.status}\n'
            text += f"• {payment.created_at.strftime('%d.%m.%Y %H:%M')}\n\n"
        await callback.message.edit_text(
            text,
            reply_markup=reply_nazad
        )
@router.callback_query(F.data == 'users_list')
async def user_list(callback:CallbackQuery):
    if not is_admin(callback.from_user.id):
        return
    with Session(bind=engine) as db:
        users = db.query(User).order_by(User.created_at.desc()).limit(20).all()
        text = '👥 Последние 20 пользователей:\n\n'
        for user in users:
            if user.subscription_end and user.subscription_end > datetime.now():
                status='✅ Активна'
            else:
                status = '❌ Неактивна'

            text += f"• ID: {user.user_id}\n"
            text += f"Подписка: {status}\n"
            if user.subscription_end:
                text += f" До: {user.subscription_end.strftime('%d.%m.%Y')}"
            if user.created_at:
                text += f"Зарегистрирован: {user.created_at.strftime('%d.%m.%Y')}\n\n"
            text += "\n"
        await callback.message.edit_text(
            text,
            reply_markup=reply_nazad
        )
@router.callback_query(F.data == 'pending_payments')
async def pending_payments(callback:CallbackQuery):
    if not is_admin(callback.from_user.id):
        return
    with Session(bind=engine) as db:
        payments = db.query(Payment).filter_by(status='pending').order_by(Payment.created_at.desc()).all()
        if not payments:
            await callback.message.edit_text(
                '⏳ Нет ожидающих платежей',
                reply_markup=reply_nazad
            )
        text = '⏳ Ожидающие платежи:\n\n'
        for payment in payments:
            text += f"• ID: {payment.id}\n"
            text += f" Пользователь: {payment.user_id}\n"
            text += f" Сумма: {payment.amount_rub}₽"
            if payment.amount_usdt and payment.amount_rub > 0:
                text += f" ({payment.amount_usdt}) USDT"
            text += f"\n Тип: {payment.product_type}\n"
            text += f" Создан: {payment.created_at.strftime('%d.%m.%Y %H:%M')}\n\n"
        await callback.message.edit_text(
            text,
            reply_markup=reply_nazad
        )
@router.callback_query(F.data == 'admin_back')
async def admin_back(callback:CallbackQuery):
    if not is_admin(callback.from_user.id):
        return
    await callback.message.edit_text("🛠️ Админ-панель:",reply_markup=keyboard)
    