import disnake
import os
import asyncio
import requests
from disnake.ext import commands
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN') # Токен бота
CHANNEL_ID = 'Ваш канал в Discord' # ID канала в Discord
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY') # API ключ YouTube
CHANNEL_YOUTUBE_ID = 'Ваш YouTube Channel ID' # ID YouTube канала

bot = commands.Bot(command_prefix="!", intents=disnake.Intents.all())

@bot.event
async def on_ready():
    print(f"Бот {bot.user} удачно запущен!")
    bot.loop.create_task(check_new_videos())  # Запуск проверки новых видео

async def send_video_notification(channel_id, video_url):
    """ Функция, которая отправляет сообщение в указанный канал с ссылкой на новое видео. """
    try:
        channel = bot.get_channel(channel_id)
        await channel.send(f"На канале вышло новое видео: {video_url}")
    except Exception as e:
        print(f"Не удалось отправить сообщение в канал {channel_id}: {e}")

async def check_new_videos():
    """ Периодически проверяет наличие новых видео на YouTube канале. """
    last_video_id = None
    while True:
        await asyncio.sleep(3600)  # Проверять каждый час
        url = f"https://www.googleapis.com/youtube/v3/search?key={YOUTUBE_API_KEY}&channelId={CHANNEL_YOUTUBE_ID}&part=snippet,id&order=date&maxResults=1"
        response = requests.get(url)
        data = response.json()
        if data['items']:
            latest_video = data['items'][0]
            video_id = latest_video['id']['videoId']
            if video_id != last_video_id:
                last_video_id = video_id
                video_url = f"https://www.youtube.com/watch?v={video_id}"
                await send_video_notification(CHANNEL_ID, video_url)

if __name__ == "__main__":
    bot.run(BOT_TOKEN)