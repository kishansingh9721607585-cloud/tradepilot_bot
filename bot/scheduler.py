from data.signals import generate_signal

CHAT_ID = None


async def alert_scan(context):
    watchlist = [
        'RELIANCE.NS',
        'TCS.NS',
        'INFY.NS'
    ]

    for stock in watchlist:
        result = generate_signal(stock)

        if result['signal'] != 'HOLD':
            msg = f"""
🚨 SIGNAL ALERT

Stock: {result['stock']}
Signal: {result['signal']}
RSI: {result['rsi']:.2f}

Reason:
{result['reason']}
"""

            if CHAT_ID:
                await context.bot.send_message(
                    chat_id=CHAT_ID,
                    text=msg
                )


def start_scheduler(app):
    # Use telegram bot's built-in job queue instead of APScheduler
    app.job_queue.run_repeating(alert_scan, interval=300, first=10)  # 5 minutes = 300 seconds