import asyncio
from aiogram import Bot, Router,F,types
from models.user import Tiket,engine
from sqlalchemy.orm import Session
from settings import ADMIN_CHAT_ID
from keyboards.inline import main_inline
from services.google_sheets import save_ticket_to_sheets
from aiogram.types import Message,ReplyKeyboardMarkup,KeyboardButton,InlineKeyboardButton,InlineKeyboardMarkup,CallbackQuery
router = Router()



async def create_tiket(user_id: int, username: str | None = None, message_text: str | None = None) -> Tiket:
    with Session(bind=engine) as db:
        tiket=Tiket(user_id=user_id,username=username,message=message_text)
        db.add(tiket)
        db.commit()
        db.refresh(tiket)
    print(">>> Пишем тикет в Sheets:", tiket.id)
    return tiket
def get_activa(user_id:int)-> Tiket:
    with Session(bind=engine) as db:
        tiket = db.query(Tiket).filter(
            Tiket.user_id == user_id,
            Tiket.status == 'open'
        ).first()
        return tiket
@router.callback_query(F.data == 'support')
async def pod(callback: CallbackQuery):
    await create_tiket(
    user_id=callback.from_user.id,
    username=callback.from_user.username,
    message_text=''
)
    await callback.message.answer('🆘 Опишите вашу проблему...')

@router.message(F.text & ~F.command & ~F.text.in_(['📊 Тарифные планы','🎫 Моя подписка','👤 Мой аккаунт','💬 Поддержка']) & ~F.text.startswith('/admin'))
async def user_message(message: Message, bot: Bot):
    tiket = await asyncio.to_thread(get_activa, message.from_user.id)
    if tiket:
        with Session(bind=engine) as db:
            db_tiket = db.query(Tiket).get(tiket.id)
            if db_tiket:
                db_tiket.message = message.text
                db.commit()
                tiket_data = {
                "id": db_tiket.id,
                "user_id": db_tiket.user_id,
                "username": db_tiket.username,
                "status": db_tiket.status,
                "created_at": db_tiket.create_at.strftime("%d.%m.%Y %H:%M") if db_tiket.create_at else "",
                "message": db_tiket.message or ""
                }
        await save_ticket_to_sheets(tiket_data)
        await bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=f'ТИКЕТ #{tiket.id}\nот: @{message.from_user.username}\nID: {message.from_user.id}\n\n💬 {message.text}'
        )
        txt = """✅ Сообщение доставлено!
Мы свяжемся с вами в ближайшее время для решения вашего вопроса"""
        await message.answer(txt)