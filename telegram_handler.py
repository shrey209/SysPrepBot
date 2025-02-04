from typing import Final
from telegram import Update
from pdf_manager import read_page
from telegram.ext import (
    Application, 
    CommandHandler, 
    ContextTypes, 
    MessageHandler, 
    filters
)



TOKEN: Final = '7849967017:AAE-AlZEB_JjLDeZsP4BvKJlv2CxuPtyE8c'
BOT_USERNAME: Final = "@SysPrepBot"

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat.id
    print(f"Chat ID: {chat_id}") 
    page=read_page()
    await update.message.reply_text(f"Hello! Thanks for chatting with me."+page)

def BotHandler():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    print("Bot is running...")
    app.run_polling()
