import os
import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.environ["BOT_TOKEN"]
ADMIN_ID = 1031700743

seen_users = set()
user_data = {}

WELCOME_MESSAGE = (
    "أهلاً و مرحباً بك في هتّان للتصاميم 🌧️🩵\n\n"
    "اختاري من القائمة ✨"
)

CONFIRM_MESSAGE = "تم استلام طلبك 🤍"

MAIN_KEYBOARD = ReplyKeyboardMarkup(
    [
        [KeyboardButton("طلب خاص 🤍")],
        [KeyboardButton("تعديل 🤍")],
        [KeyboardButton("الأسعار 🤍")],
        [KeyboardButton("اقتراح 🤍")],
        [KeyboardButton("منصاتنا 🤍")],
    ],
    resize_keyboard=True
)

MENU_RESPONSES = {
    "طلب خاص 🤍": "اكتبي طلبك بالتفصيل 🤍",
    "تعديل 🤍": "اكتبي التعديل المطلوب 🤍",
    "الأسعار 🤍": "15 ريال للصورة - 20 للفيديو 🤍",
    "اقتراح 🤍": "اكتبي اقتراحك 🤍",
    "منصاتنا 🤍": "https://t.me/hatta_n",
}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    seen_users.add(user.id)

    user_data[user.id] = {
        "id": user.id,
        "username": user.username,
        "first_name": user.first_name
    }

    await update.message.reply_text(WELCOME_MESSAGE, reply_markup=MAIN_KEYBOARD)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    if user.id == ADMIN_ID:
        return

    text = update.message.text or ""

    if text in MENU_RESPONSES:
        user_data[user.id]["last_menu"] = text
        await update.message.reply_text(MENU_RESPONSES[text])
        return

    username = f"@{user.username}" if user.username else "بدون يوزر"
    last_menu = user_data.get(user.id, {}).get("last_menu", "غير محدد")

    header = (
        f"📩 رسالة جديدة\n"
        f"👤 {username}\n"
        f"🆔 {user.id}\n"
        f"📌 القسم: {last_menu}\n\n"
        f"💬 الرسالة:\n"
    )

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=header + text
    )

    await update.message.reply_text(CONFIRM_MESSAGE)


# ⭐ نظام الرد من الأدمن (Reply)
async def reply_to_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    if not update.message.reply_to_message:
        await update.message.reply_text("⚠️ لازم تسوين Reply على رسالة المستخدم")
        return

    original = update.message.reply_to_message.text or ""

    target_user_id = None

    for line in original.splitlines():
        if "🆔" in line:
            try:
                target_user_id = int(line.split("🆔")[1].strip())
            except:
                pass

    if not target_user_id:
        await update.message.reply_text("❌ ما قدرت أحدد المستخدم")
        return

    await context.bot.send_message(
        chat_id=target_user_id,
        text=f"📬 رد من الإدارة:\n\n{update.message.text}"
    )

    await update.message.reply_text("✅ تم إرسال الرد")


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(
        MessageHandler(~filters.User(ADMIN_ID), handle_message)
    )

    app.add_handler(
        MessageHandler(filters.User(ADMIN_ID) & filters.TEXT, reply_to_user)
    )

    app.run_polling()


if __name__ == "__main__":
    main()
