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


def main():
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

    start_scheduler(app)

    app.run_polling()


if __name__ == '__main__':
    main()