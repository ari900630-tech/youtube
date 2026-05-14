import os
import time
import random
import threading
from yt_dlp import YoutubeDL

# רשימת חיפושים ממוקדת למהרג'נאת (ללא רמיקסים)
MAHRAGANAT_QUERIES = [
    "مهرجانات مصري جديد 2024",
    "أجدد مهرجانات شعبي مصري",
    "مهرجانات عصام صاصا 2024",
    "مهرجانات حמו בייקה 2024",
    "مهرجانات حسن شاקוש 2024",
    "مهرجانات حמו אלטייח'ה 2024"
]

def get_save_path():
    # בשרת של Netlify נשמור בתיקייה מקומית בשם downloads
    path = os.path.join(os.getcwd(), 'downloads')
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
    return path

class MahraganatDownloader:
    def __init__(self):
        self.save_path = get_save_path()
        self.ydl_opts = {
            # הורדה בפורמט m4a בלבד
            'format': 'bestaudio[ext=m4a]/best[ext=m4a]/best',
            # שם הקובץ: שם הזמר - שם השיר
            'outtmpl': f'{self.save_path}/%(uploader)s - %(title)s.%(ext)s',
            'ignoreerrors': True,
            'noplaylist': True,
            'match_filter': self.filter_remixes,
            'retries': 10,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }

    def filter_remixes(self, info, *, incomplete):
        title = info.get('title', '').lower()
        forbidden = ['remix', 'ريمكس', 'dj', 'دي جي', 'dance mix', 'דבקה', 'dabke']
        if any(word in title for word in forbidden):
            return "Skipping: Remix/Non-Mahraganat"
        return None

    def run(self):
        print(f"🚀 Started! Saving to: {self.save_path}")
        with YoutubeDL(self.ydl_opts) as ydl:
            while True:
                query = random.choice(MAHRAGANAT_QUERIES)
                try:
                    # חיפוש והורדה של 10 תוצאות בכל סבב
                    ydl.download([f"ytsearch10:{query}"])
                except Exception as e:
                    print(f"⚠️ Error: {e}")
                time.sleep(5) # המתנה קצרה בין סבבים

if __name__ == "__main__":
    downloader = MahraganatDownloader()
    # הרצה ב-Thread נפרד כדי שלא יחסום את השרת
    threading.Thread(target=downloader.run, daemon=True).start()
    
    # שמירה על השרת פעיל (חשוב עבור Netlify/Cloud)
    while True:
        time.sleep(100)
