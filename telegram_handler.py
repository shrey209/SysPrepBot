from typing import Final
from telegram import Update
from pdf_manager import read_page, initUser, changeBook
import os
import logging
from dotenv import load_dotenv
from llm_handler import interaction, clearPrevBookSummary, handleUserPrompt
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

# Load environment variables
load_dotenv()

TOKEN = os.getenv("TOKEN")
BOT_USERNAME = "@SysPrepBot"

# Set up logging
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat.id
    logger.info(f"Chat ID: {chat_id} started the bot.")
    initUser(chatid=chat_id)

    message = """📚 **Research Paper Bot** 🤖  

Hello! Nice to meet you.  

This bot helps you read and summarize research papers for **system design preparation**.  

🔹 **Commands:**  
- `/next` → Get the next research paper.  
- `/newpaper` → Stop the current paper and get a new one.  

If you find this bot useful, **please share it** with others! 🚀  
Happy learning! 📖"""

    await update.message.reply_text(message, parse_mode="Markdown")


async def next_page_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat.id
    logger.info(f"Next command received for Chat ID: {chat_id}")

    try:
        data = interaction(chatid=chat_id)
        await update.message.reply_text(f"{data}")
    except Exception as e:
        logger.error(f"Error in next_page_command: {e}")
        await update.message.reply_text("⚠️ An error occurred while fetching the next page. Please try again.")


async def next_book_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat.id
    try:
        changeBook(chatid=chat_id)
        logger.info(f"New book loaded for Chat ID: {chat_id}")
        clearPrevBookSummary()
        data = interaction(chatid=chat_id)
        await update.message.reply_text(f"{data}")
    except IndexError:
        await update.message.reply_text("📚 No more books available.")
    except Exception as e:
        logger.error(f"Error in next_book_command: {e}")
        await update.message.reply_text("⚠️ An error occurred while loading a new book. Please try again.")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text.lower()
    chat_id = update.message.chat.id

    try:
        data = handleUserPrompt(chatid=chat_id, userprompt=text)
        await update.message.reply_text(data)
    except Exception as e:
        logger.error(f"Error in handle_message: {e}")
        await update.message.reply_text("⚠️ An error occurred while processing your message. Please try again.")


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error(f"Exception while handling an update: {context.error}")

    # Send an error message to the user
    if update and update.message:
        await update.message.reply_text("⚠️ An unexpected error occurred. Please try again later.")


def BotHandler():
    app = Application.builder().token(TOKEN).build()

    # Command handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("newBook", next_book_command))
    app.add_handler(CommandHandler("next", next_page_command))

    # Message handler
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Error handler
    app.add_error_handler(error_handler)

    logger.info("Bot is running...")
    app.run_polling()
