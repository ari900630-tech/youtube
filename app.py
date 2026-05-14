import os
from yt_dlp import YoutubeDL

def download_from_user_query(query):
    save_path = os.path.join(os.getcwd(), 'downloads')
    if not os.path.exists(save_path):
        os.makedirs(save_path, exist_ok=True)

    ydl_opts = {
        'format': 'bestaudio[ext=m4a]/best[ext=m4a]/best',
        'outtmpl': f'{save_path}/%(uploader)s - %(title)s.%(ext)s',
        'ignoreerrors': True,
        'noplaylist': True,
        'quiet': False,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }

    with YoutubeDL(ydl_opts) as ydl:
        # מחפש ומוריד עד 100 תוצאות עבור השאילתה של המשתמש
        print(f"Searching for 100 results: {query}")
        ydl.download([f"ytsearch100:{query}"])

# פונקציה זו נקראת על ידי Netlify כאשר המשתמש לוחץ על כפתור
def handler(event, context):
    query = event.get('queryStringParameters', {}).get('q')
    if query:
        download_from_user_query(query)
        return {
            'statusCode': 200,
            'body': '{"status": "success"}'
        }
    return {
        'statusCode': 400,
        'body': '{"error": "no query provided"}'
    }
