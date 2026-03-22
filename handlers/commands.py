from aiogram import Router
from aiogram.types import Message,BotCommand
from aiogram.filters import Command
from keyboards.inline import main_inline
from sqlalchemy.orm import DeclarativeBase,Session
from sqlalchemy import Column,Integer,String,ForeignKey,create_engine,DateTime,JSON
router = Router()
product = """В NEVALASHKA есть два уровня: Путь и Сила. 
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



@router.message(Command('subscription'))
async def subscription(message:Message):
    await message.answer()
@router.message(Command('plans'))
async def plans(message:Message):
    await message.answer(product,reply_markup=main_inline)
