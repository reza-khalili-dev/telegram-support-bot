from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from datetime import datetime

# =========================
# CONFIG
# =========================

BOT_TOKEN = "8553915629:AAEe73XOkqbwsJdfaJRgGCW69Uwqws4QKt4"

#آیدی عذذی ادمین ها
ADMIN_IDS = [123456789]

# =========================
# IN-MEMORY STORAGE
# =========================

tickets = {}
user_states = {}

# =========================
# START COMMAND
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🎫 ثبت تیکت", callback_data="create_ticket")],
        [InlineKeyboardButton("ℹ️ راهنما", callback_data="help")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "👋 سلام!\n"
        "به بات پشتیبانی خوش اومدی.\n"
        "از منوی زیر انتخاب کن:",
        reply_markup=reply_markup,
    )

# =========================
# BUTTON HANDLER
# =========================

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    if query.data == "create_ticket":
        user_states[user_id] = "WAITING_FOR_TICKET"
        await query.message.reply_text(
            "🎫 ثبت تیکت\n"
            "لطفاً مشکل خودت رو در یک پیام بنویس."
        )

    elif query.data == "help":
        await query.message.reply_text(
            "ℹ️ راهنما\n"
            "• برای ثبت تیکت روی «ثبت تیکت» بزن\n"
            "• پیام مشکل رو ارسال کن\n"
            "• منتظر پاسخ پشتیبانی باش"
        )

# =========================
# MESSAGE HANDLER (TICKETS)
# =========================

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text

    # اگر کاربر در حالت ثبت تیکت نیست
    if user_states.get(user_id) != "WAITING_FOR_TICKET":
        await update.message.reply_text(
            "❗️برای ثبت تیکت، ابتدا از /start استفاده کن."
        )
        return

    ticket_id = len(tickets) + 1

    tickets[ticket_id] = {
        "user_id": user_id,
        "text": text,
        "status": "open",
        "created_at": datetime.now(),
    }

    user_states.pop(user_id)

    await update.message.reply_text(
        f"✅ تیکت شما ثبت شد.\n"
        f"شماره تیکت: #{ticket_id}\n"
        "پشتیبانی به‌زودی پاسخ می‌دهد."
    )

    # ارسال به ادمین
    for admin_id in ADMIN_IDS:
        await context.bot.send_message(
            chat_id=admin_id,
            text=(
                f"📩 تیکت جدید\n"
                f"ID: #{ticket_id}\n"
                f"User: {user_id}\n"
                f"Message:\n{text}"
            ),
        )

# =========================
# ADMIN COMMANDS
# =========================

async def admin_tickets(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    if user_id not in ADMIN_IDS:
        await update.message.reply_text("⛔️ دسترسی غیرمجاز")
        return

    if not tickets:
        await update.message.reply_text("📭 هیچ تیکتی وجود ندارد.")
        return

    message = "📋 لیست تیکت‌ها:\n\n"
    for tid, ticket in tickets.items():
        message += (
            f"#{tid} | "
            f"User: {ticket['user_id']} | "
            f"Status: {ticket['status']}\n"
        )

    await update.message.reply_text(message)

# =========================
# MAIN
# =========================

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("tickets", admin_tickets))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
