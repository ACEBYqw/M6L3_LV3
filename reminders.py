import asyncio
import json
import os
from datetime import datetime, timedelta
from discord.ext import commands
from config import REMINDERS_FILE, DATA_DIR

def get_remaining_reminders():
    """Tüm kayıtlı hatırlatmaları okur ve döndürür."""
    if os.path.exists(REMINDERS_FILE):
        with open(REMINDERS_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def save_reminders(reminders):
    """Hatırlatma listesini JSON dosyasına kaydeder."""
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(REMINDERS_FILE, "w", encoding="utf-8") as f:
        json.dump(reminders, f, ensure_ascii=False, indent=4)

def save_reminder(user_id, text, delay_seconds):
    """Yeni bir hatırlatma oluşturur ve kaydeder."""
    reminders = get_remaining_reminders()
    
    finish_time = (datetime.now() + timedelta(seconds=delay_seconds)).timestamp()
    
    new_reminder = {
        "user_id": user_id,
        "text": text,
        "finish_time": finish_time
    }
    reminders.append(new_reminder)
    reminders.sort(key=lambda x: x["finish_time"]) 
    save_reminders(reminders)

def delete_reminder(reminder_to_delete):
    """Belirli bir hatırlatmayı listeden siler."""
    reminders = get_remaining_reminders()
    
    try:
        reminders = [r for r in reminders if not (r['user_id'] == reminder_to_delete['user_id'] and r['text'] == reminder_to_delete['text'] and r['finish_time'] == reminder_to_delete['finish_time'])]
        
        save_reminders(reminders)
        return True
    except:
        return False

async def start_reminders(bot: commands.Bot):
    """Bot çalıştığı sürece hatırlatmaları kontrol eder ve gönderir."""
    await bot.wait_until_ready()
    while not bot.is_closed():
        await asyncio.sleep(5) 

        reminders = get_remaining_reminders()
        now = datetime.now().timestamp()
        
        reminders_to_keep = []
        
        for reminder in reminders:
            if reminder["finish_time"] <= now:
                user_id = int(reminder["user_id"])
                
                try:
                    user = await bot.fetch_user(user_id)
                    await user.send(f"⏰ **HATIRLATMA ZAMANI!**\nMesajınız: **{reminder['text']}**")
                except Exception as e:
                    print(f"Hatırlatma gönderilirken hata oluştu: {e}")
            else:
                reminders_to_keep.append(reminder)
        
        if len(reminders) != len(reminders_to_keep):
            save_reminders(reminders_to_keep)
