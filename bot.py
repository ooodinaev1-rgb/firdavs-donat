import telebot
from telebot import types

# ТОКЕНИ НАВРО ИНҶО ГУЗОР - он кӯҳнаро не!
BOT_TOKEN = "8888668380:AAE7uvsTTjHguh4XJvjpJQuPvsGMCBJ5BMU"
ADMIN_ID = 6602711343
DC_NUMBER = "992929611978"
ADMIN_LINK = "https://t.me/sh_donat_tj"

PRICES = {"110":10,"341":30,"572":50,"1166":99,"2398":180,"6160":460}
NAMES = {"110":"110 💎","341":"341 💎","572":"572 💎","1166":"1166 💎","2398":"2398 💎","6160":"6160 💎"}

temp = {}
bot = telebot.TeleBot(BOT_TOKEN)

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
    bot.send_message(m.chat.id, "👑💎 Firdavs DONAT💎\n\n💎 Алмазро интихоб кун:", reply_markup=kb)

@bot.callback_query_handler(func=lambda c: c.data.startswith("buy_"))
def buy(c):
    code = c.data.split("_")[1]
    temp[c.from_user.id] = code
    bot.send_message(c.message.chat.id, f"🎮 ID-ро барои {NAMES[code]} навиш:")
    bot.answer_callback_query(c.id)

@bot.message_handler(func=lambda m: m.from_user.id in temp and m.text and m.text.strip().isdigit())
def check_id(m):
    code = temp[m.from_user.id]
    gid = m.text.strip()
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("✅ Бале", callback_data=f"yes_{code}_{gid}"))
    bot.send_message(m.chat.id, f"Оё ҳамин аст:\n\n🆔 ID: {gid}\n👤 User Name: ****", reply_markup=kb)

@bot.callback_query_handler(func=lambda c: c.data.startswith("yes_"))
def yes(c):
    _, code, gid = c.data.split("_")
    temp.pop(c.from_user.id, None)
    exact = round(PRICES[code] + 0.13, 2)

    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("💳 Пардохт кардан", url=f"https://my.dc.tj/transfer?phone={DC_NUMBER}&amount={exact}"))

    bot.send_message(c.message.chat.id,
        f"Лутфан бо корти DC NEXT пардохт кунед ва сурати чекро фиристед\n\n💰 Маблағ: {exact} см",
        reply_markup=kb)

    bot.send_message(ADMIN_ID, f"🔔 Закас нав!\n👤 {c.from_user.id}\n🆔 ID: {gid}\n💎 {NAMES[code]} - {PRICES[code]} см")
    bot.answer_callback_query(c.id)

@bot.message_handler(content_types=['photo'])
def photo(m):
    kb_a = types.InlineKeyboardMarkup()
    kb_a.add(types.InlineKeyboardButton("✅ Равон шуд", callback_data=f"sent_{m.from_user.id}"))
    bot.send_photo(ADMIN_ID, m.photo[-1].file_id, caption=f"📸 ЧЕК аз {m.from_user.id}", reply_markup=kb_a)

    kb = types.InlineKeyboardMarkup(row_width=1)
    kb.add(types.InlineKeyboardButton("⏳ Интизор шавед", callback_data="wait"))
    kb.add(types.InlineKeyboardButton("📞 Ба админ муроҷиат кардан", url=ADMIN_LINK))

    bot.send_message(m.chat.id, "✅ Закасатон қабул шуд.\n\n⏳ Интизор шавед", reply_markup=kb)

@bot.callback_query_handler(func=lambda c: c.data == "wait")
def wait(c):
    bot.answer_callback_query(c.id, "⏳ 1-3 дақиқа интизор шавед!")

@bot.callback_query_handler(func=lambda c: c.data.startswith("sent_"))
def sent(c):
    uid = c.data.split("_")[1]
    bot.send_message(int(uid), "✅💎 Алмазатон равон шуд! Бозиро санҷед! 🎉")
    bot.answer_callback_query(c.id)

print("Firdavs DONAT STARTED - TANHO DC NEXT")
bot.infinity_polling(none_stop=True)