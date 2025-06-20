# Crypto Price Alert Bot
# Created by Zahid
# This bot helps users track crypto prices and get alerts on Telegram.
# Feel free to modify and use it for your crypto community!

import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
import requests
import threading
import time

TOKEN = '7960216185:AAHNL7go4ADuP9hhSIhA-bNXtLQCI3jJg4o'  # Replace with your Telegram bot token

user_alerts = {}

# Simple mapping from common symbols to CoinGecko IDs
SYMBOL_TO_ID = {
    "btc": "bitcoin",
    "eth": "ethereum",
    "bnb": "binancecoin",
    "usdt": "tether",
    "ada": "cardano",
    "doge": "dogecoin",
    "xrp": "ripple",
    "dot": "polkadot",
    "sol": "solana",
    "ltc": "litecoin",
    # add more as needed
}

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Welcome! Use /subscribe <coin_id> <target_price> to get price alerts.\n"
        "Example: /subscribe bitcoin 30000\n\n"
        "To check current price, just send the coin symbol (like BTC or ETH)."
    )

def subscribe(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    try:
        coin = context.args[0].lower()
        target_price = float(context.args[1])
    except (IndexError, ValueError):
        update.message.reply_text("Usage: /subscribe <coin_id> <target_price>\nExample: /subscribe bitcoin 30000")
        return
    
    if chat_id not in user_alerts:
        user_alerts[chat_id] = {}
    user_alerts[chat_id][coin] = target_price
    update.message.reply_text(f"Subscribed to {coin} alert at price ${target_price}")

def list_alerts(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    alerts = user_alerts.get(chat_id, {})
    if not alerts:
        update.message.reply_text("No active alerts.")
    else:
        msg = "Your alerts:\n"
        for coin, price in alerts.items():
            msg += f"- {coin}: ${price}\n"
        update.message.reply_text(msg)

def fetch_price(coin_id):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd"
    try:
        response = requests.get(url)
        data = response.json()
        return data[coin_id]['usd']
    except Exception as e:
        print(f"Error fetching price for {coin_id}: {e}")
        return None

def price_check_loop(bot):
    while True:
        for chat_id, alerts in user_alerts.items():
            for coin, target in alerts.items():
                current_price = fetch_price(coin)
                if current_price is None:
                    continue
                if current_price <= target:
                    bot.send_message(chat_id=chat_id, text=f"🚨 Alert! {coin} price is now ${current_price} <= your target ${target}")
                    # Uncomment next line if you want to remove alert after trigger
                    # del alerts[coin]
        time.sleep(60)

def handle_message(update: Update, context: CallbackContext):
    text = update.message.text.strip().lower()
    coin_id = SYMBOL_TO_ID.get(text)
    if coin_id:
        price = fetch_price(coin_id)
        if price is None:
            update.message.reply_text(f"Could not fetch price for {text.upper()} right now. Try again later.")
        else:
            update.message.reply_text(f"The current price of {text.upper()} is ${price}")
    else:
        # Optional: Comment out the line below if you don't want a reply on unknown texts
        update.message.reply_text("Send a coin symbol like BTC or ETH to get current price.")

def main():
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("subscribe", subscribe))
    dispatcher.add_handler(CommandHandler("list", list_alerts))

    # Handle plain text messages (not commands)
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()

    thread = threading.Thread(target=price_check_loop, args=(updater.bot,), daemon=True)
    thread.start()

    updater.idle()

if __name__ == "__main__":
    main()
