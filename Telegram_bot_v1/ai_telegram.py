from typing import Final
from anyio import sleep_until
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters,  ContextTypes
from dotenv import load_dotenv, find_dotenv
import os, time, pytz
from datetime import datetime, timedelta
from open_ai import Assistant
import threading
from queue import Queue
from icecream import ic

load_dotenv()
# Telegram Token and botname
TOKEN: Final = os.getenv("TELEGRAM_TOKEN")
BOT_USERNAME: Final = os.getenv('@chatmateuserbot')

#CHecking message timeout in TL
def msg_timeout(msg_time) -> bool:
    # Get the timezone object for UTC+0:00 same as TL post
    timezone = pytz.timezone('Etc/GMT+0')

    # Get the current time in the specified timezone
    current_time = datetime.now(timezone)
    current_time = current_time.replace(microsecond=0)
    
    print(f"Bot recieved message at: \t{current_time}")
    print(f"Telegram message time is: \t{msg_time}")

    # Check the timeout |change value|
    time_diff = current_time - msg_time
    
    # Check if the time difference is greater than 2 hours (7200 seconds)
    if time_diff.total_seconds() > 222:
        print(f"Message timeout FAILED. \t{time_diff.total_seconds()} seconds have passed\n")
        return False
    else:
        print(">>>Launching GPT")
        return True
    
# Call the class from open_ai
assistant_func = Assistant()

def new_id_dict(chat_id, thread_id, d=None):
    if not d:
        d = {}  # Create a new dictionary if d is not provided or is None
    d[chat_id] = thread_id  # Update the dictionary with the chat_id and thread_id
    return d

def get_chat_id(update: Update):
    chat_id = update.message.chat.id

# Gather data(in this case only time) from user's messages in TL
def message_data(msg_time, update: Update, context: ContextTypes.chat_data):
        msg_time = update.message.date
        
        return msg_time

def handle_response(text):
    user_message = text.lower() # Process the user input (if needed)
    
    if user_message:
        assistant_func.new_message(user_message)
        # assistant_func.new_run()
        # assistant_func.retrieve_run()
        response = assistant_func.list_messages()
        return response
    else:
        return "no data"

def save_message(text, chat_id, msg_time): #Creates a dict for pool.
    message_data = {
        'text': text,
        'chat_id': chat_id,
        'msg_time': msg_time
    }
    return message_data

conversation = {}
messages_pool = Queue()


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("\n_______START_______\n")

    time.sleep(1) #1 sec delay

    chat_id = update.message.chat.id    
    text: str = update.message.text
    msg_time = update.message.date

    pool_msg = save_message(text, chat_id, msg_time) #adding a data to pool

    messages_pool.put(pool_msg) #getting the message from pool
    
    thread_id = assistant_func.thread_id #Taking the thread id from class - self.thread_id

    if thread_id is None:
        ic()
        assistant_func.new_thread() #creates a new thread and return to self.thread_id
    else:
        ic()
        print("Launch the thread retrieve...")
        pass
   
    msg_check = msg_timeout(msg_time) #func timeout check
    
    print(f"User message (chat_id:{chat_id}): \t{text}") #displays user's message

    if msg_check is True:
        response: str = handle_response(text)
        thread_id = assistant_func.thread_id
        
        print("\n<<<Telegram bot answer>>>\n")
        print(f"Bot: {response:<20}\n")

        conversation = new_id_dict(chat_id, thread_id)

        print(f"Adding chat and thread ids to conversation. \nConversation: \t{conversation}")
        for key, value in conversation.items():

            print(f"chat_id: \t{key} \nthread_id: \t{value}")

        await update.message.reply_text(f"{response}")

    else:
        assistant_func.new_thread()
        thread_id = assistant_func.thread_id
        conversation = new_id_dict(chat_id, thread_id)

        print(f"Adding chat and thread ids to conversation \nConversation: \t{conversation}")
        for key, value in conversation.items():
            print(f"chat_id: \t{key} \nthread_id: \t{value}") 

        print("Bot: Message timeout. Please retry again.")
        await update.message.reply_text('Message timeout. Please retry again.')

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello there! I am here to assist you.')

async def start_thread(update: Update, context: ContextTypes.DEFAULT_TYPE):
    assistant_func.new_thread()
    await update.message.reply_text('thread')

async def start_data_collect(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('We are gathering data please wait...')
    #code here
    await update.message.reply_text('Thank you. We get all required data.') 

# Error handling
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

def main() -> None:
    print('Starting bot...')
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('thread', start_thread))
    app.add_handler(CommandHandler('get_data', start_data_collect))
    
    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors
    app.add_error_handler(error)

    # Check status every 3 sec
    print('Polling...')
    app.run_polling(poll_interval=3)

# Starting TL-bot
if __name__ == '__main__':
    main()