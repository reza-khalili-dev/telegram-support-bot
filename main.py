from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

# -----------------------------
# Bot Token (temporary)
# -----------------------------
BOT_TOKEN = "8553915629:AAEe73XOkqbwsJdfaJRgGCW69Uwqws4QKt4"

# -----------------------------
# Command Handlers
# -----------------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Runs when user sends /start command
    Shows main menu with buttons
    """

    keyboard = [
        [
            InlineKeyboardButton("🎫 ثبت تیکت", callback_data="create_ticket"),
        ],
        [
            InlineKeyboardButton("ℹ️ راهنما", callback_data="help"),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "سلام 👋\n"
        "به بات پشتیبانی خوش اومدی.\n"
        "یکی از گزینه‌های زیر رو انتخاب کن 👇",
        reply_markup=reply_markup
    )

# -----------------------------
# Main function
# -----------------------------

def main():
    """
    Start the bot
    """
    app = Application.builder().token(BOT_TOKEN).build()

    # Register command handlers
    app.add_handler(CommandHandler("start", start))

    print("🤖 Bot is running...")

    # Start polling
    app.run_polling()

# -----------------------------
# Entry point
# -----------------------------

if __name__ == "__main__":
    main()
