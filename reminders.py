# reminders.py
import os, json, asyncio
from config import DATA_DIR, REMINDERS_FILE

os.makedirs(DATA_DIR, exist_ok=True)

def save_reminder(user_id, text, delay_seconds):
    reminders = []
    if os.path.exists(REMINDERS_FILE):
        with open(REMINDERS_FILE, "r", encoding="utf-8") as f:
            try: reminders = json.load(f)
            except: reminders = []
    reminders.append({"user_id": user_id, "text": text, "delay": delay_seconds})
    with open(REMINDERS_FILE, "w", encoding="utf-8") as f:
        json.dump(reminders, f, ensure_ascii=False, indent=4)

async def start_reminders(bot):
    while True:
        reminders = []
        if os.path.exists(REMINDERS_FILE):
            with open(REMINDERS_FILE, "r", encoding="utf-8") as f:
                try: reminders = json.load(f)
                except: reminders = []

            for rem in reminders[:]:
                if rem["delay"] <= 0:
                    try:
                        user = await bot.fetch_user(rem["user_id"])
                        await user.send(f"⏰ Hatırlatma: {rem['text']}")
                    except: pass
                    reminders.remove(rem)
                else:
                    rem["delay"] -= 5

            with open(REMINDERS_FILE, "w", encoding="utf-8") as f:
                json.dump(reminders, f, ensure_ascii=False, indent=4)
        await asyncio.sleep(5)
