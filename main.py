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

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.environ["BOT_TOKEN"]
ADMIN_ID = 1031700743

seen_users: set[int] = set()
user_data: dict[int, dict] = {}

WELCOME_MESSAGE = (
    "أهلاً و مرحباً بك في هتّان للتصاميم 🌧️🩵\n"
    "سعداء جدًا بتواصلك معنا ..\n\n"
    "هنا نهتم بتفاصيلك ونصمّم لك بكل حُبّ 🤍\n\n"
    "اختاري من القائمة ..\n"
)

CONFIRM_MESSAGE = (
    "تم استلام طلبك 🤍\n"
    "وبإذن الله نرد عليك قريبًا ♥️"
)

MAIN_KEYBOARD = ReplyKeyboardMarkup(
    [
        [KeyboardButton("طلب خاص 🤍")],
        [KeyboardButton("تعديل على نماذج مُسبقة 🤍")],
        [KeyboardButton("الأسعار 🤍")],
        [KeyboardButton("اقتراحاتكم 🤍")],
        [KeyboardButton("منصاتنا 🤍")],
    ],
    resize_keyboard=True,
)

MENU_RESPONSES = {
    "طلب خاص 🤍": "اكتبي تفاصيل طلبك 🤍",
    "تعديل على نماذج مُسبقة 🤍": "ارسلي التعديل 🤍",
    "الأسعار 🤍": "تصميم الصورة 15﷼ / الفيديو 20﷼",
    "اقتراحاتكم 🤍": "نرحب باقتراحك 🤍",
    "منصاتنا 🤍": "تابعينا 🤍",
}

MENU_BUTTONS = set(MENU_RESPONSES.keys())


async def send_welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    seen_users.add(user.id)
    await update.message.reply_text(WELCOME_MESSAGE, reply_markup=MAIN_KEYBOARD)


async def handle_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    if user.id == ADMIN_ID:
        return

    text = update.message.text or ""

    if text in MENU_BUTTONS:
        await update.message.reply_text(MENU_RESPONSES[text])
        return

    header = f"رسالة من {user.first_name} (ID: {user.id})\n\n"
    await context.bot.send_message(chat_id=ADMIN_ID, text=header + text)

    await update.message.reply_text(CONFIRM_MESSAGE)


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", send_welcome))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_user))

    print("Bot running...")
    app.run_polling()


if __name__ == "__main__":
    main()
