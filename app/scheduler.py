from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.birthdays import names_for_reminder
from app.config import settings

def tomorrow_dd_mm(now: datetime | None = None, timezone: str | None = None) -> str:
    tz = ZoneInfo(timezone or settings.timezone)
    local_now = now.astimezone(tz) if now and now.tzinfo else (now.replace(tzinfo=tz) if now else datetime.now(tz))
    tomorrow = local_now.date() + timedelta(days=1)
    return tomorrow.strftime("%d-%m")

def send_tomorrow_birthday_reminder(collection, whatsapp_client) -> str | None:
    date_str = tomorrow_dd_mm()
    matches = list(collection.find({"date": date_str}, {"name": 1, "date": 1}))
    if not matches:
        return None
    names = names_for_reminder(matches)
    return f"Reminder: It's {names}'s birthday tomorrow !!"

def create_scheduler(collection, whatsapp_client):
    scheduler = AsyncIOScheduler(timezone=ZoneInfo(settings.timezone))

    async def reminder_job():
        try:
            message = send_tomorrow_birthday_reminder(collection, whatsapp_client)
            if message:
                await whatsapp_client.send_text(settings.owner_jid, message)
                print(f"Sent reminder: {message}")
            else:
                print("No birthdays for tomorrow")
        except Exception as e:
            print(f"Birthday reminder failed: {e}")
    
    scheduler.add_job(reminder_job, "cron", hour=22, minute=0, id="birthday-reminder", replace_existing=True)
    return scheduler
    