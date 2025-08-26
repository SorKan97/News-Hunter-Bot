import asyncio
import feedparser
import yaml
from telegram import Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ===== CONFIG =====
TELEGRAM_TOKEN = "7758681553:AAE4d_tBpJY1S_Nor8IvbEzFWe_mgbm-gME"
TARGET_CHAT_IDS = [67013888]
CHECK_INTERVAL = 120

# ===== LOAD FEEDS =====
with open("feeds.yml", "r", encoding="utf-8") as f:
    data = yaml.safe_load(f)
feeds = data.get("feeds", [])

# ===== TRACK SENT NEWS =====
sent_links = set()

# ===== COMMAND HANDLERS =====
async def start(update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("News Hunter Bot started! Use /id to get your chat ID.")

async def get_id(update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    await update.message.reply_text(f"Your chat ID: {chat_id}")

# ===== FETCH & SEND NEWS =====
async def fetch_and_send_news(bot: Bot):
    while True:
        for url in feeds:
            try:
                d = feedparser.parse(url)
                for entry in d.entries:
                    link = entry.get("link", "")
                    if link not in sent_links:
                        title = entry.get("title", "No title")
                        message = f"{title}\n{link}"
                        for chat_id in TARGET_CHAT_IDS:
                            await bot.send_message(chat_id=chat_id, text=message)
                        sent_links.add(link)
            except Exception as e:
                print(f"Error fetching {url}: {e}")
        await asyncio.sleep(CHECK_INTERVAL)

# ===== MAIN =====
async def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("id", get_id))

    # Start background task for news
    asyncio.create_task(fetch_and_send_news(app.bot))

    # Start bot
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
