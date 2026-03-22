from aiogram import Router,F
from aiogram.types import Message,CallbackQuery,InlineKeyboardButton,InlineKeyboardMarkup
from keyboards.inline import main_inline
import asyncio
from aiogram.fsm.context import FSMContext
from utils.states import Applications
from models.user import Applications as ApplicationModel,Session,engine
from handlers.payments import check_payment_status
from sqlalchemy.orm import DeclarativeBase,Session
from services.google_sheets import save_shits_application
router = Router()

async def start_application_fsm(message: Message, state: FSMContext):
    """Функция для запуска FSM из других файлов"""
    print("🎯 FSM запущен через функцию")
    text = (
        "Сила — это закрытый круг людей, которые уже создают результат.\n\n"
    "Чтобы попасть в Силу, нужно пройти короткую анкету: рассказать о себе, "
    "своём опыте и том, чем вы можете быть полезны другим.\n\n"
    "1. Чем вы занимаетесь сейчас и какую ценность вы создаёте?\n"
    "1–2 предложения."
    )
    await message.answer(text)
    await state.set_state(Applications.Q1)
    current_state = await state.get_state()
    print(f"🎯 Текущее состояние: {current_state}")
@router.message(Applications.Q1)
async def Q1_state(message:Message,state:FSMContext):
    print("🎯 Q1: Хендлер сработал!")
    await state.update_data(q1=message.text)
    txt = """Какой реальный результат вы сделали за последний год?
    (деньги, рост, проект, полезный навык, трансформация — что угодно, но настоящее)"""
    await message.answer(txt)
    await state.set_state(Applications.Q2)
@router.message(Applications.Q2)
async def Q2_state(message:Message,state:FSMContext):
    await state.update_data(q2=message.text)
    txt = """Чем вы можете усилить других участников?
    (компетенции, опыт, взгляд, знания, поддержка, связи — то, что вы Готовы отдавать)"""
    await message.answer(txt)
    await state.set_state(Applications.Q3)
@router.message(Applications.Q3)
async def Q3_state(message:Message,state:FSMContext):
    await state.update_data(q3=message.text)
    txt = """Зачем вам Сила?
    Почему именно сейчас и что вы хотите внутри клуба?
    (мотивация, цель, запрос)"""
    await message.answer(txt)
    await state.set_state(Applications.Q4)
@router.message(Applications.Q4)
async def Q4_state(message:Message,state:FSMContext):
    await state.update_data(q4=message.text)
    data = await state.get_data()
    answerss = {
        "q1": data.get("q1"),
        "q2": data.get("q2"),
        "q3": data.get("q3"),
        "q4": message.text,
        "username": message.from_user.username,
    }
    with Session(bind=engine) as db:
        applications = ApplicationModel(
        user_id=message.from_user.id,
        answers=data
        )
        db.add(applications)
        db.commit()
    await save_shits_application(message.from_user.id,answerss)
    await state.clear()
    await message.answer(
        "✅ Заявка отправлена на модерацию!\n"
        "Мы свяжемся с вами в течение 24 часов."
    )