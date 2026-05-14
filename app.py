import os
from googleapiclient.discovery import build
from yt_dlp import YoutubeDL

# הגדרות ה-API שלך
API_KEY = "AIzaSyAKK4VTbQJ_8tsHfxb2tcDZ9SSR9gWXH-0"

def search_and_download(query):
    try:
        # התחברות ליוטיוב
        youtube = build('youtube', 'v3', developerKey=API_KEY)

        # חיפוש הסרטון
        search_response = youtube.search().list(
            q=query,
            part='id,snippet',
            maxResults=1,
            type='video'
        ).execute()

        if not search_response['items']:
            print("לא נמצאו תוצאות.")
            return

        video_id = search_response['items'][0]['id']['videoId']
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        
        # הגדרות הורדה
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': '%(title)s.%(ext)s',
            'quiet': False,
        }

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
            print("ההורדה הושלמה בהצלחה!")

    except Exception as e:
        print(f"שגיאה: {str(e)}")

if __name__ == "__main__":
    name = input("איזה שיר להוריד? ")
    search_and_download(name)
