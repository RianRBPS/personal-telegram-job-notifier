from telegram import Bot
from config.settings import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

bot = Bot(token=TELEGRAM_BOT_TOKEN)

async def send_jobs(jobs):
    for job in jobs:
        message = f"{job['title']}\n{job['url']}\n{job['time']}"
        await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
