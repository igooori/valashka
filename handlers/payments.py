from aiogram import Router,F,Bot
from keyboards.payments_kb import inline_payments
from aiogram.types import Message,CallbackQuery,InlineKeyboardButton,InlineKeyboardMarkup,FSInputFile
from keyboards.inline import main_inline,main_inline2
from keyboards.payments_kb import inline_payments,inline_buy,inline_op,inline_otm,inline_payments_club
from handlers.commands import product
from services.payments_service import create_crypto,calculator_usdt,check_payment_status,create_yookasa,check_yookassa_status,PaymentModel
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import DeclarativeBase,Session
from models.user import Payment,engine
from services.subscription import subscription
from datetime import datetime,timedelta
from models.user import User
from handlers.applications import Applications,start_application_fsm
from aiogram.fsm.context import FSMContext
from sqlalchemy import func
from services.google_sheets import save_payment_to_sheets
router = Router()

clube_text = """Сила — закрытый уровень клуба. 
Здесь люди, которые уже создают результат: 
создают ценность, запускают проекты, развиваются и могут усиливать других. 
Чтобы войти, нужно: 
1. оформить доступ 
2. заполнить короткую анкету 
3. пройти модерацию 
Если ты не подойдёшь по уровню — 
мы переведём тебя в Путь, и доступ не потеряется. 
Если готов — выбирай способ оплаты ниже 
"""

subs_text = """"Путь — это первый уровень клуба. 
Если ты начинаешь своё движение вверх, 
хочешь повысить дисциплину, получить структуру, 
поддержку и окружение — тебе сюда. 
В Пути ты получишь: 
• базовые материалы и задания 
• регулярные разборы и ответы на вопросы 
• доступ к чату людей, которые тоже растут 
• поддержку и направление для движения 
Выбери удобный способ оплаты, 
и бот сразу откроет тебе доступ в Путь """
@router.callback_query(F.data=='subscraption')
async def subs(callback:CallbackQuery):
    await callback.message.edit_text(subs_text,reply_markup=inline_payments)
@router.callback_query(F.data.startswith('buy_'))
async def buy(callback:CallbackQuery):
    tariff = callback.data.split('_')[1]
    if tariff == '30':
        txt = """📚 Продукт: Подписка на канал «NEVALASHKA путь »

🗓 Тарифный план: 1 мес

— Период: 30 дней
— Цена: 2 000 RUB"""
    if tariff == '90':
        txt = """📚 Продукт: Подписка на канал «NEVALASHKA путь»

🗓 Тарифный план: 3 мес (-10%)

— Период: 90 дней
— Цена: 5 400 RUB"""
    if tariff == '365':
        txt = """📚 Продукт: Подписка на канал «NEVALASHKA путь»

🗓 Тарифный план: 1 год (-25%)

— Период: 365 дней
— Цена: 18 000 RUB"""
    await callback.message.edit_text(txt,reply_markup=inline_buy)
@router.callback_query(F.data=='nazad')
async def nazad(callback:CallbackQuery):
    await callback.message.edit_text(subs_text,reply_markup=inline_payments)
@router.callback_query(F.data == 'payment')
async def biu(callback:CallbackQuery):
    txt = callback.message.text
    await callback.message.edit_text(txt,reply_markup=inline_op)
@router.callback_query(F.data == 'yookas')
async def yook(callback:CallbackQuery):
    try:
        message_text = callback.message.text
        user_id = callback.from_user.id
        if "1 мес" in message_text and "2 000" in message_text:
            selected_tariff = {
                'price_rub': 2000,
                'price_usdt': calculator_usdt(2000),
                'name': 'Подписка на канал - 1 месяц',
                'type': 'put',
                'period': '30'
            }
        elif "3 мес" in message_text and "5 400" in message_text:
            selected_tariff = {
                'price_rub': 5400,
                'price_usdt': calculator_usdt(5400),
                'name': 'Подписка на канал - 3 месяца',
                'type': 'put', 
                'period': '90'
            }
        elif "1 год" in message_text and "18 000" in message_text:
            selected_tariff = {
                'price_rub': 18000,
                'price_usdt': calculator_usdt(18000),
                'name': 'Подписка на канал - 1 год',
                'type': 'put',
                'period': '365'
            }
        elif "1 мес" in message_text and "10 000" in message_text:
            selected_tariff = {
                'price_rub': 10000,
                'name': 'Участие в клубе - 1 месяц',
                'type': 'sila',
                'period': '30'
            }
        elif "3 мес" in message_text and "27 000" in message_text:
            selected_tariff = {
                'price_rub': 27000,
                'name': 'Участие в клубе - 3 месяца',
                'type': 'sila',
                'period': '90'
            }
        elif "1 год" in message_text and "90 000" in message_text:
            selected_tariff = {
                'price_rub': 90000,
                'name': 'Участие в клубе - 1 год',
                'type': 'sila',
                'period': '365'
            }
        else:
            await callback.message.answer('❌ Не удалось определить тариф')
            return
        
        print(f"👤 Пользователь {user_id} выбрал ЮKassa: {selected_tariff['name']}")
    
        payment = await create_yookasa(
            selected_tariff['price_rub'],
            selected_tariff['name'],
            user_id,
            selected_tariff['type'],
            selected_tariff['period']
        )
        if not payment:
            await callback.message.answer('❌ Ошибка создания платежа')
            return
            
        pay_url = payment.confirmation.confirmation_url
        
        
        inline_bu = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='💳 Перейти к оплате', url=pay_url)],
            [InlineKeyboardButton(text='✅ Я оплатил', callback_data=f"check_yookassa:{payment.id}")]])
        
        await callback.message.edit_text(
            f"💳 {selected_tariff['name']}\n\n"
            f"Сумма: {selected_tariff['price_rub']}₽\n\n"
            f"✅ Ссылка для оплаты готова! Нажмите кнопку ниже:\n"
            f"После оплаты нажмите 'Я оплатил'",
            reply_markup=inline_bu
        )
        
    except Exception as e:
            print(f"❌ Ошибка в обработчике: {e}")
            await callback.message.answer("❌ Произошла ошибка. Попробуйте позже.")
@router.callback_query(F.data.startswith('check_yookassa:'))
async def check_yookassa_payment(callback:CallbackQuery,state:FSMContext):
    user_id = callback.from_user.id
    payment_id = callback.data.split(':')[1]
    
    await callback.message.edit_text('🔍 Проверяем платеж ЮKassa...')
    
    is_paid = await check_yookassa_status(payment_id)
    # is_paid = True
    
    if is_paid:
        with Session(bind=engine) as db:
            payment = db.query(PaymentModel).filter_by(payment_id=payment_id).first()
            if payment:
                payment.status = 'paid'
                payment.paid_at = datetime.now()
                db.commit()
                await save_payment_to_sheets(payment)
                product_type = await subscription(
                    user_id=user_id,
                    product_type=payment.product_type,
                    period=payment.tariff_period
                )
                
                if product_type == 'put':
                    await send_subscription_access(callback, user_id, payment,state)
                else:
                    if payment.product_type == 'sila':
                        print(f"🎯 Запуск FSM для клуба, user: {user_id}")
                        await start_application_fsm(callback.message,state)
                    else:
                        await send_club_access(callback,user_id,payment,state)
            else:
                await callback.message.edit_text('❌ Ошибка: данные платежа не найдены')
    else:
        await callback.message.edit_text('❌ Платеж не найден. Если оплатили, подождите 2-3 минуты')
@router.callback_query(F.data == 'canel')
async def canel(callback:CallbackQuery):
    text = callback.message.text
    await callback.message.edit_text(text,reply_markup=inline_op)
@router.callback_query(F.data == 'crypto')
async def crypto(callback: CallbackQuery):
    try:
        user_id = callback.from_user.id
        message_text = callback.message.text
        if "1 мес" in message_text and "2 000" in message_text:
            selected_tariff = {
                'price_rub': 2000,
                'price_usdt': calculator_usdt(2000),
                'name': 'Подписка на канал - 1 месяц',
                'type': 'put',
                'period': '30'
            }
        elif "3 мес" in message_text and "5 400" in message_text:
            selected_tariff = {
                'price_rub': 5400,
                'price_usdt': calculator_usdt(5400),
                'name': 'Подписка на канал - 3 месяца',
                'type': 'put', 
                'period': '90'
            }
        elif "1 год" in message_text and "18 000" in message_text:
            selected_tariff = {
                'price_rub': 18000,
                'price_usdt': calculator_usdt(18000),
                'name': 'Подписка на канал - 1 год',
                'type': 'put',
                'period': '365'
            }
        elif "1 мес" in message_text and "10 000" in message_text:
            selected_tariff = {
                'price_rub': 10000,
                'price_usdt': calculator_usdt(10000),
                'name': 'Участие в клубе - 1 месяц',
                'type': 'sila',
                'period': '30'
            }
        elif "3 мес" in message_text and "27 000" in message_text:
            selected_tariff = {
                'price_rub': 27000,
                'price_usdt': calculator_usdt(27000),
                'name': 'Участие в клубе - 3 месяца',
                'type': 'sila',
                'period': '90'
            }
        elif "1 год" in message_text and "90 000" in message_text:
            selected_tariff = {
                'price_rub': 90000,
                'price_usdt': calculator_usdt(90000),
                'name': 'Участие в клубе - 1 год',
                'type': 'sila',
                'period': '365'
            }
        else:
            await callback.message.answer('❌ Не удалось определить тариф')
            return
        
        print(f"👤 Пользователь {user_id} выбрал: {selected_tariff['name']}")
        
        invoice = await create_crypto(
            selected_tariff['price_usdt'],
            user_id,  
            selected_tariff['type'],
            selected_tariff['period']
        )  
        if not invoice:
            await callback.message.answer('❌ Ошибка создания платежа')
            return
        pay_url = invoice.bot_invoice_url
        payment_id = invoice.invoice_id
        inline_bu = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Перейти к оплате 💰', url=pay_url)],
            [InlineKeyboardButton(text='✅ Я оплатил', callback_data=f"check_payment:{payment_id}")]])
        await callback.message.edit_text(
            f"💎 {selected_tariff['name']}\n\n"
            f"Сумма: {selected_tariff['price_rub']}₽ ({selected_tariff['price_usdt']} USDT)\n\n"
            f"✅ Инвойс создан! Нажмите для оплаты:\n"
            f"После оплаты нажмите 'Я оплатил'",
            reply_markup=inline_bu
        )
    except Exception as e:
        print(f"❌ Ошибка в обработчике: {e}")
        await callback.message.answer("❌ Произошла ошибка. Попробуйте позже.")
@router.callback_query(F.data.startswith('check_payment:'))
async def check_payment(callback:CallbackQuery,state:FSMContext):
    user_id = callback.from_user.id
    invoice_id = callback.data.split(':')[1]
    await callback.message.edit_text('🔍 Проверяем платеж...')
    is_pad = await check_payment_status(invoice_id)
    # is_pad = True
    if is_pad:
        with Session(bind=engine) as db:
            payment = db.query(Payment).filter_by(payment_id=invoice_id).first()
            if payment:
                payment.status = 'paid'
                payment.paid_at = datetime.now()
                db.commit()
                await save_payment_to_sheets(payment)
                product_type= await subscription(
                    user_id=user_id,
                    product_type=payment.product_type,
                    period=payment.tariff_period
                )
                if product_type == 'put':
                    await send_subscription_access(callback,user_id,payment,state)
                else:
                    # await send_club_access(callback, user_id, payment,state)
                    if payment.product_type == 'sila':
                        await start_application_fsm(callback.message,state)
                        print(f"🎯 Запуск FSM для клуба, user: {user_id}")
                    else:
                        await send_club_access(callback,user_id,payment,state)
            else:
                await callback.message.edit_text('❌ Ошибка: данные платежа не найдены')
    else:
            await callback.message.edit_text('❌ Платеж не найден. Если оплатили, подождите 2-3 минут')
async def  send_subscription_access(callback:CallbackQuery,user_id:int,payment:Payment,state: FSMContext | None = None):
    channel_link = 'https://t.me/+QCbDmInqL-9kYmMy'
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏔 Перейти в Путь»", url=channel_link)],
        [InlineKeyboardButton(text="💬 Поддержка", callback_data="support")]
    ])
    from datetime import datetime, timedelta
    end_date = datetime.now() + timedelta(days=int(payment.tariff_period))
    await callback.message.edit_text(
        "Вы приняты.\n"
        "Доступ к уровню Путь открыт. Добро пожаловать в круг.\n\n"
        "👇",
        reply_markup=keyboard)
async def send_club_access(callback: CallbackQuery, user_id: int, payment: Payment,state:FSMContext):
    base_link = 'https://t.me/+QCbDmInqL-9kYmMy'
    club_chat = 'https://t.me/+xym3X-IXYW82ZGY6'
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        # [InlineKeyboardButton(text="💬 Закрытый чат", url=club_chat)],
        [InlineKeyboardButton(text="📚 перейти в «AI NEVALASHKA путь» ", url=base_link)],
        [InlineKeyboardButton(text="📚 перейти в «AI NEVALASHKA сила» ", url=club_chat)],
        [InlineKeyboardButton(text="👥 Поддержка", callback_data="support")]
    ])
    from datetime import datetime, timedelta
    end_date = datetime.now() + timedelta(days=int(payment.tariff_period))
    await callback.message.edit_text(
        f'🎉 Доступ к каналу «AI NEVALASHKA сила» и «AI NEVALASHKA путь открыт»!\n\n'
        f'📅 Участие активно до: {end_date.strftime("%d.%m.%Y")}\n\n'
        f'Ваши возможности:\n'
        f'• Закрытый Telegram-чат с участниками\n'
        f'• База знаний с шаблонами и инструкциями\n'
        f'• Random Coffee с другими участниками\n'
        f'• Онлайн-встречи 2 раза в месяц\n'
        f'• Мастермайнды раз в месяц\n'
        f'• Офлайн-встречи\n\n'
        f'[Нажмите чтобы перейти в канал ]({club_chat}) «AI NEVALASHKA сила»!',
        f'[Нажмите чтобы перейти в канал ]({base_link}) «AI NEVALASHKA путь»!',
        reply_markup=keyboard,)
@router.callback_query(F.data == 'clube')
async def clube(callback:CallbackQuery):
    await callback.message.edit_text(clube_text,reply_markup=inline_payments_club)
@router.callback_query(F.data == 'clubes')
async def clube(callback:CallbackQuery):
    await callback.message.edit_caption(caption=clube_text,reply_markup=inline_payments_club)
@router.callback_query(F.data.startswith('buy:'))
async def buy(callback:CallbackQuery):
    tariff = callback.data.split(':')[1]
    if tariff == '30':
        txt = """📚 Продукт: Подписка на канал «NEVALASHKA сила»

🗓 Тарифный план: 1 мес

— Период: 30 дней
— Цена: 10 000 RUB"""
    if tariff == '90':
        txt = """📚 Продукт: Подписка на канал «NEVALASHKA сила»

🗓 Тарифный план: 3 мес (-10%)

— Период: 90 дней
— Цена: 27 000 RUB"""
    if tariff == '365':
        txt = """📚 Продукт: Подписка на канал «NEVALASHKA сила»

🗓 Тарифный план: 1 год (-25%)

— Период: 365 дней
— Цена: 90 000 RUB"""
    await callback.message.edit_text(txt,reply_markup=inline_buy)
@router.callback_query(F.data=='nazads')
async def nazads(callback:CallbackQuery):
    await callback.message.edit_text(product,reply_markup=main_inline)
async def send_reminders(bot:Bot):
    with Session(bind=engine) as db:
        soon = datetime.now() + timedelta(days=1)
        soon2 = datetime.now() + timedelta(days=3)
        subscriptions = db.query(User).filter(
            User.subscription_end.isnot(None),
            func.date(User.subscription_end) >= func.date(soon),
            func.date(User.subscription_end) <= func.date(soon2)
            ).all()
        print(f"soon: {soon}, soon2: {soon2}")
        for sub in db.query(User).all():
            print(f"subscription_end: {sub.subscription_end}")
            print(f"Найдено пользователей: {len(subscriptions)}")
        
            for sub in subscriptions:
                print(f"subscription_end: {sub.subscription_end}")
                try:
                    await bot.send_message(
                    sub.user_id,
                    f"🔔 Напоминание: ваша подписка заканчивается {sub.subscription_end.strftime('%d.%m.%Y')}\n\n"
                    f"Продлите доступ, чтобы не прервать участие!"
                )
                except Exception as e:
                    print(f"Не удалось отправить напоминание {sub.user_id}: {e}")
async def reminder_scheduler(bot):
    while True:
        try:
            await send_reminders(bot)
            print("✅ Проверка напоминаний завершена")
        except Exception as e:
            print(f"❌ Ошибка в планировщике напоминаний: {e}")
        
        await asyncio.sleep(24 * 60 * 60) 

    


