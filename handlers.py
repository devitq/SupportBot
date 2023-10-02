import emoji as emoji
from datetime import datetime	
from telegram.ext import CommandHandler, MessageHandler, Filters
from replit import db
from settings import TELEGRAM_SUPPORT_CHAT_ID
import os

if not os.path.exists('recieving.txt'):
     file=open("recieving.txt", "x")
     file.write("1")
     file.close()
mess_time={}
mess={}

def start(update, context):
    lang_emoji = emoji.lang_emoji(update.message.from_user.language_code)
    if not str(update.message.from_user.id) in db:
        db[update.message.from_user.id] = 0
        update.message.reply_text(f"Здравствуйте, {update.message.from_user.first_name}!\n\nЭто бот для технической поддержки. Вопросы обрабатываются в порядке живой очереди, поэтому постарайтесь вложить всю суть своего вопроса в одном сообщении.")
        text=f"\nid: ```{update.message.from_user.id}```\nИмя: {update.message.from_user.first_name}\nЯзык: {lang_emoji}"
        context.bot.send_message(
            chat_id=TELEGRAM_SUPPORT_CHAT_ID,
            text=f"📞 Подключён пользователь:{text}", parse_mode='MarkdownV2')
        forwarded = update.message.forward(chat_id=TELEGRAM_SUPPORT_CHAT_ID)
        context.bot.send_message(
            chat_id=TELEGRAM_SUPPORT_CHAT_ID,
            reply_to_message_id=forwarded.message_id,
            text=f'{update.message.from_user.id}\n💬 Новое сообщение:{text}\nУ вас новое сообщение, смахните влево это сообщение и ответьте пользователю', parse_mode='MarkdownV2'
        )
    else:
        update.message.reply_text(f"И снова здравствуйте, {update.message.from_user.first_name}!\n\nЭто бот для технической поддержки. Вопросы обрабатываются в порядке живой очереди, поэтому постарайтесь вложить всю суть своего вопроса в одном сообщении.")

def forward_to_chat(update, context):    
    lang_emoji = emoji.lang_emoji(update.message.from_user.language_code)
    f = open("recieving.txt")
    t=f.read()
    f.close()
    if update.message.from_user.id not in mess_time:
        mess[update.message.from_user.id] = 0
        mess_time[update.message.from_user.id] = datetime.now()
    delta=datetime.now()-mess_time[update.message.from_user.id]
    if delta.total_seconds()>60:
        mess[update.message.from_user.id] = 0
        mess_time[update.message.from_user.id] = datetime.now()
    if mess[update.message.from_user.id] == 0 and db[str(update.message.from_user.id)] == 0 and t=="1":
        forwarded = update.message.forward(chat_id=TELEGRAM_SUPPORT_CHAT_ID)
        mess_time[update.message.from_user.id]=datetime.now()
        text=f"\nid: ```{update.message.from_user.id}```\nИмя: {update.message.from_user.first_name}\nЯзык: {lang_emoji}"   
        context.bot.send_message(
            chat_id=TELEGRAM_SUPPORT_CHAT_ID,
            reply_to_message_id=forwarded.message_id, text=f'{update.message.from_user.id}\n💬 Новое сообщение:{text}\nУ вас новое сообщение, смахните влево это сообщение и ответьте пользователю', parse_mode='MarkdownV2')
        context.bot.send_message(chat_id=update.message.from_user.id, text='✅️ Отправлено')
        mess[update.message.from_user.id]=1
    elif t=="0":
    	context.bot.send_message(chat_id=update.message.from_user.id, text='⛔️ Оператор запретил отправку сообщений.')
    elif db[str(update.message.from_user.id)] == 1:
    	context.bot.send_message(chat_id=update.message.from_user.id, text='⛔️ Вы заблокированы, ваше сообщение не будет отправлено оператору.')
    else:
    	context.bot.send_message(chat_id=update.message.from_user.id, text=f'⚠️ Во избежании спама вы можете отправлять сообщение только раз в минуту, подождите ещё {int(60-delta.total_seconds())} секунд(ы).')

def help(update, context):
	help_text='''
Команды оператора:
/help - Вывести это сообщение
/toggle_recieving - Переключить отправку сообщений
/users - Список поьзователей
/ban {id} - Заблокировать пользователя с {id}
/unban {id} - Разблокировать пользователя с {id}
/ban_user - Блокирует пользователя, на сообщение которого вы ответили
/unban_user - Разблокирует пользователя, на сообщение которого вы ответили
'''
	context.bot.send_message(chat_id=TELEGRAM_SUPPORT_CHAT_ID, text=help_text)

def toggle_recieving(update, context):
    f = open("recieving.txt")
    t=f.read()
    f.close()
    if t=="1":
        f = open("recieving.txt", "w")
        f.write("0")
        f.close()
        context.bot.send_message(chat_id=TELEGRAM_SUPPORT_CHAT_ID, text='Вы выключили отправку сообщений')
    else:
        f = open("recieving.txt", "w")
        f.write("1")
        f.close()
        context.bot.send_message(chat_id=TELEGRAM_SUPPORT_CHAT_ID, text='Вы включили отправку сообщений')

def users(update, context):
    msg='Все пользователи:\n\n'
    for key in db:
        if db[key]==1:
            msg+=f'id: ```{key}```, статус: заблокирован\n'
        elif db[key]==0:
            msg+=f'id: ```{key}```, статус: разблокирован\n'
    if msg=='Все пользователи:\n\n':
        msg+='не найдено подключённых пользователей ☹️'
    context.bot.send_message(chat_id=TELEGRAM_SUPPORT_CHAT_ID, text=msg, parse_mode='MarkdownV2')

def ban(update, context):
    try:
        id=int(context.args[0])
        if str(id) in db:
            if db[str(id)]==0:
                db[str(id)]=1
                context.bot.send_message(chat_id=TELEGRAM_SUPPORT_CHAT_ID, text=f"Пользователь с id: ```{str(id)}``` успешно заблокирован", parse_mode='MarkdownV2')
                context.bot.send_message(chat_id=int(id), text=f'⛔️ Вы заблокированы, теперь ваши сообщения не будут отправляться оператору.')
            else:
                context.bot.send_message(chat_id=TELEGRAM_SUPPORT_CHAT_ID, text=f'Пользователь с id: ```{str(id)}``` уже заблокирован', parse_mode='MarkdownV2')
        else:
            context.bot.send_message(chat_id=TELEGRAM_SUPPORT_CHAT_ID, text=f"Пользователь с id: ```{str(id)}``` не найден", parse_mode='MarkdownV2')
    except:
        context.bot.send_message(chat_id=TELEGRAM_SUPPORT_CHAT_ID, text="Вы не указали id пользователя или id, которое вы ввели не является числом")

def unban(update, context):
    try:
        id=int(context.args[0])
        if str(id) in db:
            if db[str(id)]==1:
                db[str(id)]=0
                context.bot.send_message(chat_id=TELEGRAM_SUPPORT_CHAT_ID, text=f"Пользователь с id: ```{id}``` успешно разблокирован", parse_mode='MarkdownV2')
                context.bot.send_message(chat_id=int(id), text=f'✅ Вы разблокированы, теперь ваши сообщения будут отправляться оператору.')
            else:
                context.bot.send_message(chat_id=TELEGRAM_SUPPORT_CHAT_ID, text=f"Пользователь с id: ```{id}``` уже разблокирован", parse_mode='MarkdownV2')
        else:
            context.bot.send_message(chat_id=TELEGRAM_SUPPORT_CHAT_ID, text=f"Пользователь с id: ```{id}``` не найден", parse_mode='MarkdownV2')
    except:
        context.bot.send_message(chat_id=TELEGRAM_SUPPORT_CHAT_ID, text="Вы не указали id пользователя или id, которое вы ввели не является числом")

def forward_to_user(update, context):
    user_id = None
    if "У вас новое сообщение, смахните влево это сообщение и ответьте пользователю" in update.message.reply_to_message.text:
        try:
            user_id = int(update.message.reply_to_message.text.split('\n')[0])
        except ValueError:
            user_id = None
    if user_id and update.message.text!='/ban_user' and update.message.text!='/unban_user':
        context.bot.copy_message(
            message_id=update.message.message_id,
            chat_id=user_id,
            from_chat_id=update.message.chat_id
        )
        context.bot.send_message(chat_id=TELEGRAM_SUPPORT_CHAT_ID, text='✅ Отправлено')
    elif update.message.text=='/ban_user' or update.message.text=='/unban_user' and user_id:
        if update.message.text=='/ban_user':
            if db[str(user_id)]==0:
                db[user_id] = 1
                context.bot.send_message(
            chat_id=TELEGRAM_SUPPORT_CHAT_ID,
            text=f'Пользователь с id: ```{user_id}``` успешно заблокирован', parse_mode='MarkdownV2')
                context.bot.send_message(chat_id=int(user_id), text=f'⛔️ Вы заблокированы, теперь ваши сообщения не будут отправляться оператору.')
            else:
               context.bot.send_message(chat_id=TELEGRAM_SUPPORT_CHAT_ID, text=f"Пользователь с id: ```{user_id}``` уже заблокирован", parse_mode='MarkdownV2') 
        else:
            if db[str(user_id)]==1:
                db[user_id] = 0
                context.bot.send_message(
                chat_id=TELEGRAM_SUPPORT_CHAT_ID,
                text=f'Пользователь с id: ```{user_id}``` успешно разблокирован', parse_mode='MarkdownV2')
                context.bot.send_message(chat_id=user_id, text=f'✅ Вы разблокированы, теперь ваши сообщения будут отправляться оператору.')
            else:
                context.bot.send_message(chat_id=TELEGRAM_SUPPORT_CHAT_ID, text=f"Пользователь с id: ```{user_id}``` уже разблокирован", parse_mode='MarkdownV2')
    else:
        context.bot.send_message(
            chat_id=TELEGRAM_SUPPORT_CHAT_ID,
            text="Ошибка, вы смахнули не то сообщение!"
        )

def setup_dispatcher(dp):
    dp.add_handler(CommandHandler('start', start, Filters.chat_type.private))
    dp.add_handler(CommandHandler('users', users, Filters.chat(TELEGRAM_SUPPORT_CHAT_ID)))
    dp.add_handler(CommandHandler('ban', ban, Filters.chat(TELEGRAM_SUPPORT_CHAT_ID)))
    dp.add_handler(CommandHandler('unban', unban, Filters.chat(TELEGRAM_SUPPORT_CHAT_ID)))
    dp.add_handler(CommandHandler('help', help, Filters.chat(TELEGRAM_SUPPORT_CHAT_ID)))
    dp.add_handler(CommandHandler('toggle_recieving', toggle_recieving, Filters.chat(TELEGRAM_SUPPORT_CHAT_ID)))
    dp.add_handler(MessageHandler(Filters.chat_type.private, forward_to_chat))
    dp.add_handler(MessageHandler(Filters.chat(TELEGRAM_SUPPORT_CHAT_ID) & Filters.reply, forward_to_user))
    return dp