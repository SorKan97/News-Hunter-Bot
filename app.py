# app.py
import asyncio
import yaml
from telegram.ext import ApplicationBuilder, CommandHandler
import feedparser

# ========================
# Configuration
# ========================
TELEGRAM_TOKEN = "7758681553:AAE4d_tBpJY1S_Nor8IvbEzFWe_mgbm-gME"
CHAT_ID = 67013888

FEEDS_FILE = "feeds.yml"

# ========================
# Load RSS feeds
# ========================
def load_feeds():
    with open(FEEDS_FILE, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    feeds = data.get("feeds", [])
    if not feeds:
        print("Warning: No feeds found in feeds.yml")
    return feeds

# ========================
# Functions
# ========================
async def fetch_and_send_news(application):
    feeds = load_feeds()
    for url in feeds:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            await application.bot.send_message(
                chat_id=CHAT_ID,
                text=f"{entry.title}\n{entry.link}"
            )

async def start_command(update, context):
    await update.message.reply_text("Bot is running!")

# ========================
# Main Application
# ========================
async def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Add /start command
    app.add_handler(CommandHandler("start", start_command))

    # Fetch RSS once at startup
    app.create_task(fetch_and_send_news(app))

    # Start bot
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    await app.updater.idle()
    await app.stop()
    await app.shutdown()

# ========================
# Entry point
# ========================
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
