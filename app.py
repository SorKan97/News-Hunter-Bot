import asyncio
import feedparser
import yaml
from telegram import Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# --- CONFIG ---
TELEGRAM_TOKEN = "7758681553:AAE4d_tBpJY1S_Nor8IvbEzFWe_mgbm-gME"
TARGET_CHAT_IDS = [67013888]  # <-- Add your Telegram chat ID(s) here

# --- NEWS FEEDS ---
with open("feeds.yml", "r") as f:
    FEEDS = yaml.safe_load(f)

# --- COMMAND HANDLERS ---
async def start(update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot is running!")

# --- FETCH & SEND NEWS ---
async def fetch_and_send_news(bot: Bot):
    while True:
        for feed_name, url in FEEDS.items():
            d = feedparser.parse(url)
            if d.entries:
                latest = d.entries[0].title
                for chat_id in TARGET_CHAT_IDS:
                    await bot.send_message(chat_id=chat_id, text=f"{feed_name}: {latest}")
        await asyncio.sleep(3600)  # repeat every 1 hour

# --- MAIN ---
async def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))

    # Start news task
    asyncio.create_task(fetch_and_send_news(app.bot))

    # Run bot
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
