from aiogram.fsm.state import State,StatesGroup
class UserForm(StatesGroup):
    fio = State()
    email = State()
    phone = State()
    confirm = State()
class Applications(StatesGroup):
    Q1 = State()
    Q2 = State()
    Q3 = State()
    Q4 = State()