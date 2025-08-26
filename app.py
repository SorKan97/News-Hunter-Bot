import asyncio
import feedparser
import yaml
import html
from telegram import Bot
from telegram.ext import ApplicationBuilder

# ====== CONFIG ======
TELEGRAM_TOKEN = "7758681553:AAE4d_tBpJY1S_Nor8IvbEzFWe_mgbm-gME"
CHAT_ID = 67013888
FEEDS_FILE = "feeds.yml"

# ====== Load feeds ======
with open(FEEDS_FILE, "r", encoding="utf-8") as f:
    data = yaml.safe_load(f)
feeds = data.get("feeds", [])

if not feeds:
    print("No feeds found in feeds.yml. Exiting.")
    exit(1)


async def fetch_and_send_news(bot: Bot):
    for url in feeds:
        try:
            if isinstance(url, list):
                url = url[0]
            d = feedparser.parse(str(url))
            for entry in d.entries[:5]:
                title = html.escape(entry.title)
                link = entry.link
                message = f"*{title}*\n{link}"
                await bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="Markdown")
        except Exception as e:
            print(f"Error fetching/sending feed {url}: {e}")


async def scheduler(bot: Bot):
    while True:
        await asyncio.sleep(3600)  # every hour
        await fetch_and_send_news(bot)


async def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    bot = app.bot

    # Run fetch once at start
    await fetch_and_send_news(bot)

    # Schedule repeated fetching
    app.create_task(scheduler(bot))

    # Start bot polling (this handles its own event loop!)
    await app.run_polling()


# ✅ Instead of asyncio.run(), call main() directly
if __name__ == "__main__":
    import nest_asyncio
    nest_asyncio.apply()  # allows event loop to work on Render
    asyncio.get_event_loop().run_until_complete(main())
