import logging
import yaml
import feedparser
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    filters, ContextTypes
)

# -------------------- CONFIG --------------------
TELEGRAM_TOKEN = '7758681553:AAE4d_tBpJY1S_Nor8IvbEzFWe_mgbm-gME'
FEEDS_FILE = 'feeds.yml'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
chat_ids = set()

# -------------------- LOAD FEEDS --------------------
with open(FEEDS_FILE, 'r', encoding='utf-8') as f:
    feeds = yaml.safe_load(f)['feeds']

# -------------------- HANDLERS --------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    chat_ids.add(chat_id)
    await update.message.reply_text(
        f"Hello! Your chat ID is {chat_id}. You will start receiving news shortly."
    )

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id not in chat_ids:
        chat_ids.add(chat_id)
        await update.message.reply_text(f"Got your chat ID: {chat_id}. You are added.")

# -------------------- FETCH NEWS --------------------
async def fetch_and_send_news(context: ContextTypes.DEFAULT_TYPE):
    for feed in feeds:
        parsed_feed = feedparser.parse(feed['url'])
        if parsed_feed.entries:
            for entry in parsed_feed.entries[:3]:  # Top 3 entries per feed
                for chat_id in chat_ids:
                    await context.bot.send_message(
                        chat_id=chat_id,
                        text=f"{feed['name']}:\n{entry.title}\n{entry.link}"
                    )

# -------------------- MAIN --------------------
def main():
    if not TELEGRAM_TOKEN:
        raise RuntimeError("TELEGRAM_TOKEN is required")

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Send news immediately after /start
    async def immediate_news(context: ContextTypes.DEFAULT_TYPE):
        for chat_id in chat_ids:
            for feed in feeds:
                parsed_feed = feedparser.parse(feed['url'])
                if parsed_feed.entries:
                    for entry in parsed_feed.entries[:3]:
                        await context.bot.send_message(
                            chat_id=chat_id,
                            text=f"{feed['name']}:\n{entry.title}\n{entry.link}"
                        )

    # Job queue for hourly news
    app.job_queue.run_repeating(fetch_and_send_news, interval=3600, first=10)

    logger.info("Bot started. Waiting for messages to get chat ID...")
    app.run_polling()

if __name__ == '__main__':
    main()
