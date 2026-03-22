from dotenv import load_dotenv
from os import getenv
load_dotenv()
TOKEN=getenv('TOKEN')
ADMIN_ID = [int(getenv('ADMIN_ID'))]
ADMIN_CHAT_ID = int(getenv('ADMIN_ID'))
CRYPTOBOT_TOKEN=getenv('CRYPTOBOT_TOKEN')
YOOKASSA_ACCOUNT_ID=int(getenv('YOOKASSA_ACCOUNT_ID'))
YOOKASSA_SECRET_KEY=getenv('YOOKASSA_SECRET_KEY')
