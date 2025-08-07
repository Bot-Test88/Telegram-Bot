import os
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
API_URL = "https://api16-normal-c-useast1a.tiktokv.com/aweme/v1/feed/"

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("🎬 TikTok Video Downloader Bot!\nএকটি TikTok লিংক পাঠান")

def handle_tiktok_link(update: Update, context: CallbackContext) -> None:
    try:
        url = update.message.text
        video_id = url.split('/video/')[1].split('?')[0]
        api_data = requests.get(f"{API_URL}?aweme_id={video_id}").json()
        video_url = api_data['aweme_list'][0]['video']['play_addr']['url_list'][0]
        update.message.reply_video(video=video_url)
    except Exception as e:
        update.message.reply_text(f"❌ ত্রুটি: {str(e)}")

def main():
    updater = Updater(TELEGRAM_TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_tiktok_link))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
