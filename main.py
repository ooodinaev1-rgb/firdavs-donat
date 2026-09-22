import telebot
from telebot import types

# ========= НАСТРОИКА =========
BOT_TOKEN = "8888668380:AAE7uvsTTjHguh4XJvjpJQuPvsGMCBJ5BMU"
ADMIN_ID = 6602711343
DC_NUMBER = "992929611978"
ADMIN_LINK = "https://t.me/sh_donat_tj"

PRICES = {
    "110": 10,
    "341": 30,
    "572": 50,
    "1166": 99,
    "2398": 180,
    "6160": 460
}
NAMES = {
    "110": "110 💎",
    "341": "341 💎",
    "572": "572 💎",
    "1166": "1166 💎",
    "2398": "2398 💎",
    "6160": "6160 💎"
}

temp = {}
bot = telebot.TeleBot(BOT_TOKEN)

# ========= START =========
@bot.message_handler(commands=['start'])
def start(m):
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(
        types.InlineKeyboardButton("💎 110 - 10см", callback_data="buy_110"),
        types.InlineKeyboardButton("💎 341 - 30см", callback_data="buy_341"),
        types.InlineKeyboardButton("💎 572 - 50см", callback_data="buy_572"),
        types.InlineKeyboardButton("💎 1166 - 99см", callback_data="buy_1166"),
        types.InlineKeyboardButton("💎 2398 - 180см", callback_data="buy_2398"),
        types.InlineKeyboardButton("💎 6160 - 460см", callback_data="buy_6160"),
    )
    bot.send_message(m.chat.id,
        "👑💎 Firdavs DONAT💎 💎👑\n\n"
        "🔥 Хуш омадед!\n"
        "⚡ Равонкунӣ 1-5 дақиқа\n\n"
        "👇 Алмазро интихоб кун:",
        reply_markup=kb)

# ========= ИНТИХОБ =========
@bot.callback_query_handler(func=lambda c: c.data.startswith("buy_"))
def buy(c):
    code = c.data.split("_")[1]
    temp[c.from_user.id] = code
    bot.send_message(c.message.chat.id, f"🎮 ID барои {NAMES[code]}-ро навиш:\n💡 Мисол: 123456789")
    bot.answer_callback_query(c.id)

# ========= САНҶИШИ ID =========
@bot.message_handler(func=lambda m: m.from_user.id in temp and m.text and m.text.strip().isdigit())
def check_id(m):
    code = temp[m.from_user.id]
    gid = m.text.strip()
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("✅ Бале", callback_data=f"yes_{code}_{gid}"))
    bot.send_message(m.chat.id,
        f"🔍 Оё ҳамин аст:\n\n"
        f"🆔 ID: {gid}\n"
        f"👤 User Name: ****\n"
        f"💎 {NAMES[code]} - {PRICES[code]} см",
        reply_markup=kb)

# ========= ПАРДОХТ - БЕ ХАТОГӢ =========
@bot.callback_query_handler(func=lambda c: c.data.startswith("yes_"))
def yes(c):
    _, code, gid = c.data.split("_")
    temp.pop(c.from_user.id, None)
    exact = round(PRICES[code] + 0.13, 2)

    kb = types.InlineKeyboardMarkup(row_width=1)
    kb.add(types.InlineKeyboardButton(f"📋 Копи: {DC_NUMBER}", callback_data="copy"))
    kb.add(types.InlineKeyboardButton("📱 DC NEXT кушодан", url="https://play.google.com/store/apps/details?id=tj.dushanbecity.dcnext"))

    bot.send_message(c.message.chat.id,
        f"🙏💳 Лутфан бо DC NEXT пардохт кун ва чек фирист 💳🙏\n\n"
        f"📱 Номер: `{DC_NUMBER}`\n"
        f"💰 Маблағ: {exact} см\n"
        f"🎮 ID: {gid}\n"
        f"💎 {NAMES[code]}\n\n"
        f"1️⃣ Копи пахш кун\n"
        f"2️⃣ Дар DC ба ҳамин номер {exact} см равон кун\n"
        f"3️⃣ Чекашро ин ҷо фирист 📸",
        parse_mode="Markdown", reply_markup=kb)

    bot.send_message(ADMIN_ID, f"🔔 Закас нав!\n👤 {c.from_user.id}\n🆔 {gid}\n💎 {NAMES[code]} {exact}см")
    bot.answer_callback_query(c.id)

@bot.callback_query_handler(func=lambda c: c.data == "copy")
def copy(c):
    bot.answer_callback_query(c.id, f"📋 {DC_NUMBER} копи шуд!", show_alert=True)

# ========= ЧЕК =========
@bot.message_handler(content_types=['photo'])
def photo(m):
    kb_a = types.InlineKeyboardMarkup()
    kb_a.add(types.InlineKeyboardButton("✅ Равон шуд", callback_data=f"sent_{m.from_user.id}"))
    bot.send_photo(ADMIN_ID, m.photo[-1].file_id, caption=f"📸 ЧЕК аз {m.from_user.id}", reply_markup=kb_a)

    kb = types.InlineKeyboardMarkup(row_width=1)
    kb.add(types.InlineKeyboardButton("⏳ Интизор мешавам", callback_data="wait"))
    kb.add(types.InlineKeyboardButton("📞 Муроҷиат ба админ", callback_data="to_admin"))

    bot.send_message(m.chat.id, "✅ Закасатон қабул шуд.\n\n⏳ Интизор шавед", reply_markup=kb)

@bot.callback_query_handler(func=lambda c: c.data == "wait")
def wait(c):
    bot.send_message(c.message.chat.id, "хуб ман дар наздиктарин фурсат донат мекунам🙂")
    bot.answer_callback_query(c.id)

@bot.callback_query_handler(func=lambda c: c.data == "to_admin")
def to_admin(c):
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("📞 Ба админ гузаштан", url=ADMIN_LINK))
    bot.send_message(c.message.chat.id, "📞 Ба админ:", reply_markup=kb)
    bot.answer_callback_query(c.id)

@bot.callback_query_handler(func=lambda c: c.data.startswith("sent_"))
def sent(c):
    uid = c.data.split("_")[1]
    bot.send_message(int(uid), "✅💎 Алмазатон равон шуд! Бозиро санҷед! 🎉")
    bot.answer_callback_query(c.id)

print("Firdavs DONAT STARTED - NO ERROR")
bot.infinity_polling(none_stop=True, interval=0)