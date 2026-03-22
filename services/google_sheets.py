import gspread
from google.oauth2.service_account import Credentials
import asyncio
from datetime import datetime
from models.user import Payment,Tiket
_spreadsheet = None

def setup_shets():
    global _spreadsheet
    try:
        if _spreadsheet is not None:
            return _spreadsheet

        scope = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive',
        ]
        creds = Credentials.from_service_account_file('credentials.json', scopes=scope)
        client = gspread.authorize(creds)

        sheet_id = '1Tj7qE3o2P87dRkklpQ-8pJQne-Teqk0Vuvfx6rZiMp8'
        _spreadsheet = client.open_by_key(sheet_id) 

        print('✅ Гугл шитс подключен')
        return _spreadsheet

    except Exception as e:
        print('❌ Ошибка гугл шитс:',e)
        
        return None

async def get_worksheet(name: str):
    spreadsheet = await asyncio.to_thread(setup_shets)
    if not spreadsheet:
        return None
    return spreadsheet.worksheet(name)
async def save_shits_application(user_id: int, answerss: dict):
    try:
        print('💾 Сохраняем анкету Силы:', user_id, answerss)
        ws = await get_worksheet('Applications')
        if not ws:
            return False
        row_data = [
            str(user_id),
            answerss.get("q1", ""),        
            answerss.get("q2", ""),        
            answerss.get("q3", ""),        
            answerss.get("q4", ""),        
            answerss.get("username", ""),  
            datetime.now().strftime("%d.%m.%Y %H:%M"),  
            "на модерации",               
        ]

        await asyncio.to_thread(ws.append_row, row_data)
        print(f"✅ Анкета Силы сохранена в Sheets для user_id: {user_id}")
        return True
    except Exception as e:
        print(f"❌ Ошибка сохранения анкеты в Sheets: {e}")
        return False
async def save_payment_to_sheets(payment: Payment):
    try:
        ws = await get_worksheet('Payments')
        if not ws:
            return False
        row = [
            str(payment.user_id),
            payment.payment_id,
            payment.amount_rub or 0,
            payment.amount_usdt or 0,
            payment.currency or "",
            payment.payment_system or "",
            payment.status or "",
            payment.product_type or "",
            payment.tariff_period or "",
            payment.created_at.strftime("%d.%m.%Y %H:%M") if payment.created_at else "",
            payment.paid_at.strftime("%d.%m.%Y %H:%M") if payment.paid_at else "",
            "PAYMENT",
        ]
        await asyncio.to_thread(ws.append_row, row)
        return True
    except Exception as e:
        print('❌ Ошибка save_payment_to_sheets:', e)
        return False
async def save_ticket_to_sheets(tiket_data: dict):
    try:
        ws = await get_worksheet("Tickets")
        if not ws:
            return False

        row = [
            str(tiket_data.get("id", "")),
            str(tiket_data.get("user_id", "")),
            tiket_data.get("username", ""),
            tiket_data.get("status", ""),
            tiket_data.get("created_at", ""),
            tiket_data.get("message", ""),
            "TICKET",
        ]
        await asyncio.to_thread(ws.append_row, row)
        return True
    except Exception as e:
        print("❌ Ошибка save_ticket_to_sheets:", e)
        return False
async def save_shits(user_data:dict):
    try:
        print('💾 Сохранить данные:', user_data)

        ws = await get_worksheet('Users')
        if not ws:
            return False

        row_data = [
            str(user_data.get('user_id', '')),
            user_data.get('registration_date', ''),
            user_data.get('subscription_end', ''),
        ]

        await asyncio.to_thread(ws.append_row, row_data)
        print(f"✅ Данные сохранены для user_id: {user_data['user_id']}")
        return True
    except Exception as e:
        print('❌ Ошибка сохранения:', e)
        return False