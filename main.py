from flask import Flask
from threading import Thread
import os

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler
)

from config import BOT_TOKEN

from bot.commands import (
    start,
    help_command,
    market,
    signal,
    chart,
    crypto,
    gold,
    addstock_command,
    removestock_command,
    portfolio_command
)

from bot.scheduler import start_scheduler


# Flask app
web_app = Flask(__name__)

@web_app.route('/')
def home():
    return "Bot is running!"


# Telegram bot function
def run_bot():

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('market', market))
    app.add_handler(CommandHandler('signal', signal))
    app.add_handler(CommandHandler('chart', chart))
    app.add_handler(CommandHandler('crypto', crypto))
    app.add_handler(CommandHandler('gold', gold))
    app.add_handler(CommandHandler('addstock', addstock_command))
    app.add_handler(CommandHandler('removestock', removestock_command))
    app.add_handler(CommandHandler('portfolio', portfolio_command))

    print("🚀 Trading Bot Running...")

    # start_scheduler(app)

    print("BOT TOKEN:", BOT_TOKEN)
    print("Polling started")

    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":

    # Start telegram bot in background
    bot_thread = Thread(target=run_bot)
    bot_thread.start()

    # Start Flask web server
    port = int(os.environ.get("PORT", 10000))

    web_app.run(
        host="0.0.0.0",
        port=port,
        debug=False,
        use_reloader=False
    )
