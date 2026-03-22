from aiogram import Router,F,Bot
from aiogram.types import Message,CallbackQuery,BotCommand,FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from sqlalchemy.orm import Session
from handlers.commands import product
from keyboards.inline import main_inline,main_inline2
from models.user import User
from utils.states import UserForm
from models.user import engine
from services.google_sheets import save_shits
from datetime import datetime

router = Router()
hello_txt = f"""Добро пожаловать в NEVALASHKA. 
Это клуб для тех, кто выбирает путь роста — 
путь к силе, свободе и лучшей версии себя. 
Здесь собираются те, кто поднимает свой уровень, 
действует и усиливает друг друга. 
У нас есть два уровня: 
Путь - Для тех, кто сейчас строит себя. 
Основы дисциплины, знаний и среды, которая не даёт сдаться. 
Сила - Закрытый круг людей, которые уже создают результат и готовы усиливать друг 
друга. 
Выберите, что вам ближе — и бот направит вас дальше. """
# photo = FSInputFile("nevalashka_bot/photo_img/Frame_50.png")
photo = FSInputFile("photo.png")
@router.callback_query(F.data == 'levels_info')
async def levels(callback:CallbackQuery):
    txt = """В NEVALASHKA есть два уровня: Путь и Сила. 
Путь — стартовое движение. 
Если ты хочешь поднять дисциплину, навести порядок в себе, 
начать стабильный рост и попасть в окружение людей, 
которые стремятся шагнуть выше, но ещё не делают сильных результатов — 
начинай с Пути. 
Сила — следующий уровень. 
Если ты уже создаёшь результат, растёшь в деле, 
обладаешь экспертизой и готов усиливать других — 
можешь подать заявку в Силу. 
Выбери, что подходит тебе сейчас 
"""
    await callback.message.answer_photo(photo=photo,caption=txt)
    await callback.message.answer('Выберите действие ниже 👇', reply_markup=main_inline2)
@router.message(Command('start'))
async def start(message:Message,state:FSMContext,bot:Bot):
    user = message.from_user
    with Session(bind=engine) as db:
        db_user = db.query(User).filter_by(user_id=user.id).first()
        if not db_user:
            db_user = User(user_id=user.id)
            db.add(db_user)
            db.commit()
            await save_shits(db_user)

    await message.answer_photo(photo=photo,caption=hello_txt)
    await message.answer('Выберите действие ниже 👇', reply_markup=main_inline)



        
    