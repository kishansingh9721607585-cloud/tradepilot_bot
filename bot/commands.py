from telegram import Update
from telegram.ext import ContextTypes

from data.market_data import get_market_data
from data.signals import generate_signal
from data.charts import generate_chart

from portfolio.portfolio_manager import (
    add_stock,
    remove_stock,
    get_portfolio
)


from bot.scheduler import CHAT_ID

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    global CHAT_ID

    CHAT_ID = update.effective_chat.id

    msg = """
🚀 TRADING BOT ACTIVE

Commands:

/market
/signal STOCK
/chart STOCK
/crypto
/gold
/addstock STOCK
/removestock STOCK
/portfolio
/help
"""

    await update.message.reply_text(msg)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "Use /signal reliance or /chart tcs"
    )


async def market(update: Update, context: ContextTypes.DEFAULT_TYPE):

    data = get_market_data()

    msg = "📊 LIVE MARKET\n\n"

    for item in data:

        emoji = "🟢" if item['change'] > 0 else "🔴"

        msg += (
            f"{emoji} {item['name']}\n"
            f"Price: {item['price']:.2f}\n"
            f"Change: {item['change']:.2f}%\n\n"
        )

    await update.message.reply_text(msg)


async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:

        stock = context.args[0].upper()

        if '.NS' not in stock:
            stock += '.NS'

        result = generate_signal(stock)

        if 'error' in result:
            await update.message.reply_text(result['error'])
            return

        emoji = {
            'BUY': '🟢',
            'SELL': '🔴',
            'HOLD': '🟡'
        }

        msg = f"""
📈 STOCK SIGNAL

Stock: {result['stock']}
Price: ₹{result['price']:.2f}
RSI: {result['rsi']:.2f}

{emoji[result['signal']]} {result['signal']}

Reason:
{result['reason']}
"""

        await update.message.reply_text(msg)

    except:

        await update.message.reply_text(
            "Example:\n/signal reliance"
        )


async def chart(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:

        stock = context.args[0].upper()

        if '.NS' not in stock:
            stock += '.NS'

        path = generate_chart(stock)

        await update.message.reply_photo(
            photo=open(path, 'rb')
        )

    except:

        await update.message.reply_text(
            "Example:\n/chart reliance"
        )


async def crypto(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "Use /signal BTC-USD"
    )


async def gold(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "Gold symbol: GC=F\nSilver symbol: SI=F"
    )


async def addstock_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:

        stock = context.args[0].upper()

        user_id = update.effective_user.id

        add_stock(user_id, stock)

        await update.message.reply_text(
            f"✅ Added {stock}"
        )

    except:

        await update.message.reply_text(
            "Usage:\n/addstock TCS"
        )


async def removestock_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:

        stock = context.args[0].upper()

        user_id = update.effective_user.id

        remove_stock(user_id, stock)

        await update.message.reply_text(
            f"❌ Removed {stock}"
        )

    except:

        await update.message.reply_text(
            "Usage:\n/removestock TCS"
        )


async def portfolio_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    stocks = get_portfolio(user_id)

    if not stocks:

        await update.message.reply_text(
            "Portfolio empty"
        )

        return

    msg = "📂 YOUR PORTFOLIO\n\n"

    for stock in stocks:
        msg += f"• {stock}\n"

    await update.message.reply_text(msg)
