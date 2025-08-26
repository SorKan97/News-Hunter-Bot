import asyncio
from telegram import Bot

# Replace with your token and chat ID
TOKEN = "7758681553:AAE4d_tBpJY1S_Nor8IvbEzFWe_mgbm-gME"
CHAT_ID = 123456789

async def main():
    bot = Bot(token=TOKEN)
    await bot.send_message(chat_id=CHAT_ID, text="Hello! Bot is working!")
    await bot.session.close()  # cleanly close connection

# Run the async function
asyncio.run(main())
