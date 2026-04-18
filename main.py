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
    "هنا نهتم بتفاصيلك ونصمّم لك بكل حُبّ و نشاركك تفاصيل مُناسبتك السّعيدة 🤍\n\n"
    "اختاري من القائمة ما يناسبك ..\n"
    "أو شاركينا فكرتك و طلبك بكل بساطة\n\n"
    "و بإذن الله نرد عليك بأقرب وقت\n\n"
    "شكراً لـ ثقتك في هتان و نسعد بخدمتك دائمًا 🤍"
)

CONFIRM_MESSAGE = (
    "تم استلام طلبك بكل حُبّ 🤍\n\n"
    "شكرًا لتواصلك معنا ..\n"
    "وبإذن الله نردّ عليك في أقرب وقت ممكن\n"
    "نقدّر ثقتك في هتان ♥️"
)

MAIN_KEYBOARD = ReplyKeyboardMarkup(
    [
        [KeyboardButton("طلب خاص 🤍")],
        [KeyboardButton("تعديل على نماذج مُسبقة 🤍")],
        [KeyboardButton("الأسعار 🤍")],
        [KeyboardButton("اقتراحاتكم و مُلاحظاتكم 🤍")],
        [KeyboardButton("منصاتنا 🤍")],
    ],
    resize_keyboard=True,
    is_persistent=True,
)

MENU_RESPONSES = {
    "طلب خاص 🤍": (
        "تسعدنا خدمتك 🤍\n\n"
        "اكتبي تفاصيل طلبك \"الفكرة + نوع المُناسبة + أي مُلاحظات تهمك\"\n\n"
        "و بإذن الله نتواصل معك على الخاص -التليجرام- لتنفيذها بكل حّب ♥️"
    ),
    "تعديل على نماذج مُسبقة 🤍": (
        "بكل حب جاهزين لخدمتك ..\n\n"
        "ارسلي الطلب المُراد التعديل عليه، واكتبي نوع التعديل المطلوب بالتفصيل\n\n"
        "و بإذن الله نتواصل معك على الخاص -التليجرام- لتنفيذها بكل حّب ♥️"
    ),
    "الأسعار 🤍": (
        "🏷️ الأسعار\n\n"
        "تصميم الصورة : 15 ﷼\n"
        "تصميم الفيديو : 20 ﷼\n\n"
        "وبإذن الله نخدمك بكل حب ♥️"
    ),
    "اقتراحاتكم و مُلاحظاتكم 🤍": (
        "رأيك محل ثقتنا و إهتمامنا .. 🌧️\n\n"
        "اكتبي لنا أي فكرة أو ملاحظة في بالك\n"
        "فكل كلمة منك وقود لتطورنا\n\n"
        "نسعد بك وشكرًا لثقتك في هتان ♥️"
    ),
    "منصاتنا 🤍": (
        "تابعينا على حساباتنا الرسمية لتكوني مُطّلعه\n"
        "على جديدنا و أعمالنا ..\n\n"
        "قناة التليجرام : https://t.me/hatta_n\n"
        "حساب التيك توك : https://www.tiktok.com/@hatta_nn\n\n"
        "وجودك معنا يسعدنا، وشكرًا لدعمك لـ هتان ♥️"
    ),
}

MENU_BUTTONS = set(MENU_RESPONSES.keys())

REPLY_LABELS = {
    "طلب خاص 🤍": "ردًا على طلبك الخاص 🤍",
    "تعديل على نماذج مُسبقة 🤍": "ردًا على طلب التعديل 🤍",
    "الأسعار 🤍": "ردًا على استفساركِ عن الأسعار 🤍",
    "اقتراحاتكم و مُلاحظاتكم 🤍": "ردًا على اقتراحاتكِ 🤍",
    "منصاتنا 🤍": "ردًا على استفساركِ عن منصاتنا 🤍",
    "طلب غير محدد": "رد من الإدارة 🤍",
}


async def send_welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    user_data[user.id] = {
        "id": user.id,
        "first_name": user.first_name,
        "username": user.username,
    }

    seen_users.add(user.id)

    await update.message.reply_text(WELCOME_MESSAGE, reply_markup=MAIN_KEYBOARD)


first_name}\n"
        f"اليوزر: {username_display}\n"
        f"الـ ID: {user.id}\n"
        f"─────────────────\n"
        f"{last_menu}\n"
    )

    if update.message.text:
        await context.bot.send_message(chat_id=ADMIN_ID, text=header + update.message.text)
    elif update.message.photo:
        await context.bot.send_photo(
            chat_id=ADMIN_ID,
            photo=update.message.photo[-1].file_id,
            caption=header,
        )
    elif update.message.video:
        await context.bot.send_video(
            chat_id=ADMIN_ID,
            video=update.message.video.file_id,
            caption=header,
        )
    elif update.message.document:
        await context.bot.send_document(
            chat_id=ADMIN_ID,
            document=update.message.document.file_id,
            caption=header,
        )
    elif update.message.voice:
        await context.bot.send_voice(
            chat_id=ADMIN_ID,
            voice=update.message.voice.file_id,
            caption=header,
        )
    elif update.message.sticker:
        await context.bot.send_message(chat_id=ADMIN_ID, text=header + "[ستيكر]")
        await context.bot.send_sticker(
            chat_id=ADMIN_ID,
            sticker=update.message.sticker.file_id,
        )
    else:
        await context.bot.send_message(chat_id=ADMIN_ID, text=header + "[رسالة غير مدعومة]")

    await update.message.reply_text(CONFIRM_MESSAGE)


async def reply_to_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        await update.message.reply_text("⚠️ لازم تردين على رسالة المستخدم")
        return

    replied_text = update.message.reply_to_message.text or ""

    target_user_id = None
    lines = replied_text.splitlines()

    for line in lines:
        if "ID:" in line:
            try:
                target_user_id = int(line.split("ID:")[1].strip())
            except:
                pass

    if not target_user_id:
        await update.message.reply_text("❌ ما قدرت أحدد المستخدم")
        return

    await context.bot.send_message(
        chat_id=target_user_id,
        text=f"📬 رد الإدارة:\n\n{update.message.text}",
    )

    await update.message.reply_text("✅ تم الإرسال")


async def list_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    if not user_data:
        await update.message.reply_text("لا يوجد مستخدمين")
        return

    text = "\n".join(
        [f"{u['first_name']} - {u.get('username')} - {uid}" for uid, u in user_data.items()]
    )

    await update.message.reply_text(text)


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", send_welcome))
    app.add_handler(CommandHandler("users", list_users))

    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND & filters.User(ADMIN_ID), reply_to_user)
    )

    app.add_handler(
        MessageHandler(~filters.User(ADMIN_ID), handle_user_message)
    )

    app.run_polling()


if name == "__main__":
    main()


async def reply_to_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        await update.message.reply_text("⚠️ لازم تردين على رسالة المستخدم")
        return

    replied_text = update.message.reply_to_message.text or ""

    target_user_id = None
    lines = replied_text.splitlines()

    for line in lines:
        if "ID:" in line:
            try:
                target_user_id = int(line.split("ID:")[1].strip())
            except:
                pass

    if not target_user_id:
        await update.message.reply_text("❌ ما قدرت أحدد المستخدم")
        return

    await context.bot.send_message(
        chat_id=target_user_id,
        text=f"📬 رد الإدارة:\n\n{update.message.text}",
    )

    await update.message.reply_text("✅ تم الإرسال")


async def list_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    if not user_data:
        await update.message.reply_text("لا يوجد مستخدمين")
        return

    text = "\n".join(
        [f"{u['first_name']} - {u.get('username')} - {uid}" for uid, u in user_data.items()]
    )

    await update.message.reply_text(text)


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", send_welcome))
    app.add_handler(CommandHandler("users", list_users))

    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND & filters.User(ADMIN_ID), reply_to_user)
    )

    app.add_handler(
        MessageHandler(~filters.User(ADMIN_ID), handle_user_message)
    )

    app.run_polling()


if name == "__main__":
    main()
