# crypto_alert_bot

# Crypto Price Alert Bot

Created by Zahid.

A simple Telegram bot to get price alerts for cryptocurrencies using the CoinGecko API.

## Features

- Subscribe to price alerts for any coin supported by CoinGecko.
- Set target prices to receive Telegram notifications.
- List your active alerts.
- Runs continuously and checks prices every minute.

## Setup

1. Create a Telegram bot using [BotFather](https://t.me/BotFather) and get the API token.

2. Clone this repository or download the files.

3. Install dependencies:

```bash
pip install -r requirements.txt


Usage
/start - Show welcome message.

/subscribe <coin> <price> - Set an alert.
Example: /subscribe bitcoin 30000

/list - List your active alerts.

Send coin symbol like BTC to get the current price.


