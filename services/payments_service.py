from aiocryptopay import AioCryptoPay,Networks
from aiogram import Router,F
from settings import CRYPTOBOT_TOKEN,YOOKASSA_ACCOUNT_ID,YOOKASSA_SECRET_KEY
from aiogram.types import Message,CallbackQuery,InlineKeyboardButton,InlineKeyboardMarkup
from models.user import Payment as PaymentModel,engine
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import DeclarativeBase,Session
import yookassa
from services.google_sheets import save_payment_to_sheets
from yookassa import Payment as YooPayment,Configuration
import uuid
router = Router()
RATE = 81
def calculator_usdt(price_rub:float) -> float:
    return round(price_rub / RATE,3)
cryptopay = AioCryptoPay(
    token=CRYPTOBOT_TOKEN,
    network=Networks.MAIN_NET 
)
async def create_crypto(amount: float, user_id: int, product_type: str, tariff: str):
    try:
        invoice = await cryptopay.create_invoice(
            asset='USDT',
            amount=amount
        )
        await asyncio.to_thread(save_payment_to_db, invoice, user_id, amount, product_type, tariff)
        print(f"✅ Инвойс создан: {invoice.invoice_id}")
        return invoice
    except Exception as e:
        print('Ошибка создания инвойса:', e)
        return None
def save_payment_to_db(invoice, user_id: int, amount: float, product_type: str, tariff: str):
    with Session(bind=engine) as db:
        new_payment = PaymentModel(
            user_id=user_id,
            payment_id=invoice.invoice_id,
            amount_rub=amount * 81,
            amount_usdt=amount,
            currency='USDT',
            payment_system='cryptopay',
            status='pending',
            product_type=product_type,
            tariff_period=tariff
        )
        db.add(new_payment)
        db.commit()
        
async def check_payment_status(invoice_id: str):
    try:
        invoices = await cryptopay.get_invoices(invoice_ids=invoice_id)
        if invoices and invoices[0].status == "paid":
            return True
        return False
    except Exception as e:
        print(f"Ошибка проверки платежа: {e}")
        return False
Configuration.account_id = YOOKASSA_ACCOUNT_ID
Configuration.secret_key = YOOKASSA_SECRET_KEY
async def create_yookasa(amount:float,description:str,user_id:int,product_type: str, period: str):
    try:
        id_key = str(uuid.uuid4())
        payment = YooPayment.create({
            'amount':{
                'value':f'{amount:.2f}',
                'currency': 'RUB',
            },
            'confirmation': {
                'type': 'redirect',
                'return_url': 'https://t.me/nevalashka_bot'
            },
            'capture': True,
            'description': description,
            'metadata': {
                'user_id': user_id,
                'product_type': product_type,
                'period':period
            }
        },id_key)
        await asyncio.to_thread(
            save_yookassa_payment_to_db,payment,user_id,amount,product_type,period
        )
        return payment
    except Exception as e:
        print('ошибка', e)
        return None
def save_yookassa_payment_to_db(payment, user_id: int, amount: float, product_type: str, period: str):
    with Session(bind=engine) as db:
        new_payment = PaymentModel(
            user_id=user_id,
            payment_id=payment.id,
            amount_rub=amount,
            amount_usdt=0,
            currency='RUB', 
            payment_system='yookassa',
            status='pending',
            product_type=product_type,  
            tariff_period=period,       
        )
        db.add(new_payment)
        db.commit()
async def check_yookassa_status(payment_id: str):
    try:
        payment = YooPayment.find_one(payment_id)
        
        if payment.status == 'succeeded':
            with Session(bind=engine) as db:
                db_payment = db.query(PaymentModel).filter_by(payment_id=payment_id).first()
                if db_payment:
                    db_payment.status = 'paid'
                    db.commit()
                    print(f"✅ Платеж ЮKassa подтвержден: {payment_id}")
            return True
            
        return False
    except Exception as e:
        print(f"❌ Ошибка проверки платежа ЮKassa: {e}")
        return False