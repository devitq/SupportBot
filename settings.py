import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

BOT_TOKEN = os.getenv("BOT_TOKEN")
TELEGRAM_SUPPORT_CHAT_ID = int(os.getenv("TELEGRAM_SUPPORT_CHAT_ID"))