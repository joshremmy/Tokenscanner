import os
import re

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    MessageHandler,
    ContextTypes,
    filters,
)

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is missing.")

ETH_PATTERN = re.compile(r"\b0x[a-fA-F0-9]{40}\b")
SOL_PATTERN = re.compile(r"\b[1-9A-HJ-NP-Za-km-z]{32,44}\b")

seen = set()


async def scan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    text = update.message.text or ""

    contracts = ETH_PATTERN.findall(text)
    contracts += SOL_PATTERN.findall(text)

    if not contracts:
        return

    for contract in contracts:

        if contract in seen:
            continue

        seen.add(contract)

        print(f"Detected: {contract}")

        await update.message.reply_text(
            f"📡 Token detected!\n\n<code>{contract}</code>",
            parse_mode="HTML"
        )


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, scan)
    )

    print("Bot started...")

    app.run_polling()


if __name__ == "__main__":
    main()
