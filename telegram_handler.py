from typing import Final
from telegram import Update
from pdf_manager import read_page, initUser
import os
from llm_handler import interaction
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

load_dotenv()
from dotenv import load_dotenv

TOKEN: Final = os.getenv("TOKEN")
BOT_USERNAME: Final = "@SysPrepBot"


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat.id
    print(f"Chat ID: {chat_id}")
    initUser(chatid=chat_id)
    await update.message.reply_text(f"Hello! nice to meet you to start seeing the research papers type /next")
    


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


def BotHandler():
    app = Application.builder().token(TOKEN).build()

    # Command and message handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("next", next_page_command))  # New /next handler
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is running...")
    app.run_polling()
