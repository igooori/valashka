import asyncio 
from aiogram import Bot,Dispatcher
from settings import TOKEN
from aiogram.types import BotCommand,MenuButtonCommands
from aiogram.fsm.storage.memory import MemoryStorage
from handlers.admin import router as admin_router
from handlers.commands import router as start_router
from handlers.profile import router as profile_router
from handlers.payments import router as payments_router
from handlers.support import router as support_router
from handlers.applications import router as applications_router
from handlers.payments import reminder_scheduler
async def set_menu(bot:Bot):
    await bot.set_chat_menu_button(menu_button=MenuButtonCommands(type='commands'))
async def set_my_commands(bot:Bot):
    commands = [
    BotCommand(command='plans',description='купить подписку'),
    BotCommand(command='start', description='👋 Начать работу / Приветствие')
]
    await bot.set_my_commands(commands)

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())
async def main():
    dp.include_router(admin_router)
    dp.include_router(start_router)
    dp.include_router(profile_router)
    dp.include_router(applications_router)
    dp.include_router(payments_router)
    dp.include_router(support_router)
    asyncio.create_task(reminder_scheduler(bot))
    await set_menu(bot)
    await set_my_commands(bot)
    print('бот запущен')
    await dp.start_polling(bot)
asyncio.run(main())