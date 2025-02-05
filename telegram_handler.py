from typing import Final
from telegram import Update
from pdf_manager import read_page, initUser,changeBook
import os
from dotenv import load_dotenv
from llm_handler import interaction,clearPrevBookSummary,handleUserPrompt
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

load_dotenv()

TOKEN = os.getenv("TOKEN")
print(TOKEN)
BOT_USERNAME = "@SysPrepBot"

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat.id
    print(f"Chat ID: {chat_id}")
    initUser(chatid=chat_id)
    await update.message.reply_text(f"Hello! Nice to meet you. To start reading research papers, type /next.")


async def send_welcome_message(context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = context.job.data
    await context.bot.send_message(chat_id=chat_id, text="Hello, nice to meet you!")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat.id
    user_message = update.message.text
    print(f"User message: {user_message}, Chat ID: {chat_id}")

    data = interaction(chatid=chat_id)
    await update.message.reply_text(f"{data}")


async def next_page_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
   
    chat_id = update.message.chat.id
    print(f"Next command received for Chat ID: {chat_id}")

    data = interaction(chatid=chat_id)
    await update.message.reply_text(f"{data}")

async def next_book_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat.id
    try:
        changeBook(chatid=chat_id)
        print("New book")
        clearPrevBookSummary()
        data = interaction(chatid=chat_id)
        await update.message.reply_text(f"{data}")
    except IndexError:
        await update.message.reply_text("No more books available.")



async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text.lower()
    chat_id=update.message.chat.id
    data=handleUserPrompt(chatid=chat_id,userprompt=text)
    await update.message.reply_text(data)



def BotHandler():
    app = Application.builder().token(TOKEN).build()

    # Command and message handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("newBook",next_book_command))
    app.add_handler(CommandHandler("next", next_page_command))  # New /next handler
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    

    print("Bot is running...")
    app.run_polling()
