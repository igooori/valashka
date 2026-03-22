from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from models.user import User,engine,Payment
import asyncio
from services.google_sheets import save_shits
async def subscription(user_id:int,product_type:str,period:str):
    with Session(bind=engine) as db:
        days = int(period)
        end_date = datetime.now() + timedelta(days=days)
        user = db.query(User).filter_by(user_id=user_id).first()
        if not user:
            user = User(user_id=user_id,subscription_end=end_date)
            db.add(user)
        else:
            user.subscription_end=end_date
        payment = db.query(Payment).filter_by(
            user_id=user_id,
            status='pending'
        ).order_by(Payment.created_at.desc()).first()
        if payment:
            payment.status = 'paid'
            payment.paid_at = datetime.now()
        db.commit()
        user_data = {
            "user_id": user_id,
            "registration_date": user.created_at.strftime("%d.%m.%Y %H:%M") if user.created_at else "",
            "subscription_end": user.subscription_end.strftime("%d.%m.%Y %H:%M") if user.subscription_end else "",
        }  
    await save_shits(user_data)
    print(f"✅ Доступ выдан user_id {user_id} на {days} дней")
    return product_type
