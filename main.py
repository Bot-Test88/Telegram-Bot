import os
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
API_URL = "https://api16-normal-c-useast1a.tiktokv.com/aweme/v1/feed/"

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("📲 TikTok Downloader Bot!\nSend me a TikTok link")

def handle_tiktok_link(update: Update, context: CallbackContext) -> None:
    try:
        video_id = update.message.text.split('/video/')[1].split('?')[0]
        api_response = requests.get(f"{API_URL}?aweme_id={video_id}").json()
        video_url = api_response['aweme_list'][0]['video']['play_addr']['url_list'][0]
        update.message.reply_video(video=video_url)
    except Exception as e:
        update.message.reply_text(f"❌ Error: {str(e)}")

def main():
    updater = Updater(TELEGRAM_TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_tiktok_link))
    
    # Render-specific webhook setup
    PORT = int(os.environ.get('PORT', 5000))
    updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TELEGRAM_TOKEN)
    updater.bot.set_webhook(f"https://your-app-name.onrender.com/{TELEGRAM_TOKEN}")
    updater.idle()

if __name__ == '__main__':
    main()
