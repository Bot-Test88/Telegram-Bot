import os
import requests
from telegram import Update, InputMediaPhoto
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Configuration
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
API_URL = "https://api.tiktokv.com/aweme/v1/aweme/detail/"  # Public API endpoint

# Start command handler
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "Hello! Send me a TikTok video link and I'll download it for you with its caption!"
    )

# Handle TikTok links
def handle_tiktok_link(update: Update, context: CallbackContext) -> None:
    message = update.message
    url = message.text
    
    if "tiktok.com" not in url:
        message.reply_text("Please send a valid TikTok video URL.")
        return
    
    try:
        # Extract video ID from URL
        video_id = extract_video_id(url)
        if not video_id:
            raise ValueError("Could not extract video ID")
        
        # Get video info from API
        video_data = get_video_data(video_id)
        if not video_data:
            raise ValueError("Could not fetch video data")
        
        # Get video URL and caption
        video_url = video_data['video']['play_addr']['url_list'][0]
        caption = video_data['desc']
        
        # Download and send the video
        message.reply_video(
            video=video_url,
            caption=caption,
            supports_streaming=True
        )
        
    except Exception as e:
        print(f"Error: {e}")
        message.reply_text("Sorry, I couldn't download that video. Please try another one.")

def extract_video_id(url: str) -> str:
    # This is a simplified version - you might need a more robust URL parser
    if "/video/" in url:
        return url.split("/video/")[1].split("?")[0]
    return None

def get_video_data(video_id: str) -> dict:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(f"{API_URL}?aweme_id={video_id}", headers=headers)
    return response.json()

def main() -> None:
    # Create the Updater and pass it your bot's token.
    updater = Updater(TELEGRAM_TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Register commands
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_tiktok_link))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C
    updater.idle()

if __name__ == '__main__':
    main()
