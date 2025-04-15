import os
import nest_asyncio
import asyncio
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    MessageHandler,
    filters,
)

# Apply nest_asyncio to reuse existing loop
nest_asyncio.apply()

# Your bot token (set this in Replit Secrets)
TOKEN = os.getenv("TOKEN")

# ARM / DISARM keyboard
keyboard = [['ARM', 'DISARM']]
reply_markup = ReplyKeyboardMarkup(
    keyboard,
    resize_keyboard=True,
    one_time_keyboard=False
)

# Handle incoming messages (no reply, only shows keyboard for unknown messages)
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip().upper()
    if text not in ("ARM", "DISARM"):
        await update.message.reply_text(
            "Tap below to control the system:",
            reply_markup=reply_markup
        )
    # else: Do nothing for ARM/DISARM

# Main bot function
async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    print("🤖 Bot is running...")
    await app.run_polling()

# Run using existing event loop
asyncio.get_event_loop().run_until_complete(main())
