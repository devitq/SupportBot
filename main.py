from telegram.ext import Updater
from handlers import setup_dispatcher
from settings import BOT_TOKEN
from web_app import keep_alive
from replit import db
def delete():
    for key in db:
        del db[key]

updater = Updater(BOT_TOKEN)

#delete()
keep_alive()
dp = updater.dispatcher
dp = setup_dispatcher(dp)
updater.start_polling()
updater.idle()