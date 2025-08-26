import asyncio
import feedparser
import yaml
from telegram import Bot
from telegram.ext import ApplicationBuilder

# ====== CONFIG ======
TELEGRAM_TOKEN = "7758681553:AAE4d_tBpJY1S_Nor8IvbEzFWe_mgbm-gME"
CHAT_ID = 67013888  # your chat ID
FEEDS_FILE = "feeds.yml"

# ====== Load feeds ======
with open(FEEDS_FILE, "r", encoding="utf-8") as f:
    data = yaml.safe_load(f)
feeds = data.get("feeds", [])

if not feeds:
    print("No feeds found in feeds.yml. Exiting.")
    exit(1)


# ====== Async function to fetch news and send ======
async def fetch_and_send_news(bot: Bot):
    for url in feeds:
        try:
            # Make sure url is a string
            if isinstance(url, list):
                url = url[0]
            d = feedparser.parse(str(url))
            for entry in d.entries[:5]:  # send only latest 5 items per feed
                message = f"*{entry.title}*\n{entry.link}"
                await bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="Markdown")
        except Exception as e:
            print(f"Error fetching/sending feed {url}: {e}")


# ====== Main async function ======
async def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    bot = app.bot

    # Run fetch_and_send_news once at start
    await fetch_and_send_news(bot)

    # Schedule it every hour
    async def scheduler():
        while True:
            await asyncio.sleep(3600)  # 1 hour
            await fetch_and_send_news(bot)

    # Create task for scheduler
    app.create_task(scheduler())

    # Start polling
    await app.run_polling()


if __name__ == "__main__":
    asyncio.run(main())
