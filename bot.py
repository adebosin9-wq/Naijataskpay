import logging, threading, os
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = "8807153787:AAGGOaHHGTvtseSZLJ2-7WKbJboaqjDe9TY"
users = {}
logging.basicConfig(level=logging.INFO)
web = Flask(__name__)

@web.route('/')
def home(): return "Bot is Live!"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if uid not in users:
        users[uid] = {"balance": 0, "referrals": 0}
        if context.args:
            try:
                ref = int(context.args[0])
                if ref in users and ref != uid:
                    users[ref]["balance"] += 500
                    users[ref]["referrals"] += 1
                    await context.bot.send_message(ref, "New referral! +500")
            except: pass
    botname = (await context.bot.get_me()).username
    link = f"https://t.me/{botname}?start={uid}"
    await update.message.reply_text(f"Welcome! Balance: N{users[uid]['balance']}\nReferrals: {users[uid]['referrals']}\n\nYOUR LINK:\n{link}")

async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bal = users.get(update.effective_user.id, {}).get("balance", 0)
    await update.message.reply_text(f"Balance: N{bal}")

async def referrals(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    botname = (await context.bot.get_me()).username
    link = f"https://t.me/{botname}?start={uid}"
    await update.message.reply_text(f"Referrals: {users.get(uid, {}).get('referrals',0)}\n{link}")

def run_bot():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("balance", balance))
    app.add_handler(CommandHandler("referrals", referrals))
    app.run_polling()

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    web.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
