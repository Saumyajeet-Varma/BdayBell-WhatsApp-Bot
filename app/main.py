from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.commands import CommandHandler
from app.config import settings
from app.database import connect_db, close_db
from app.scheduler import create_scheduler
from app.whatsapp import WhatsAppClient

@asynccontextmanager
async def lifespan(app: FastAPI):
    collection = connect_db()
    whatsapp = WhatsAppClient(settings.session_dir, on_text=lambda text, jid: handler.handle(text, jid))
    handler = CommandHandler(collection, whatsapp)
    scheduler = create_scheduler(collection, whatsapp)
    scheduler.start()
    app.state.collection = collection
    app.state.whatsapp = whatsapp
    app.state.scheduler = scheduler
    try:
        if settings.whatsapp_enabled:
            await whatsapp.start()
        yield
    finally:
        scheduler.shutdown(wait=False)
        await whatsapp.stop()
        close_db()

app = FastAPI(title="BDayBell", version="0.1.0", lifespan=lifespan)

@app.get("/ping")
def ping():
    return "Bot is Alive !!"

@app.get("/health")
def health():
    return {"status": "ok", "whatsapp_enabled": settings.whatsapp_enabled}