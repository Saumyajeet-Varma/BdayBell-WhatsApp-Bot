import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Settings:
    port: int = int(os.getenv("PORT", "3000"))
    mongo_uri: str = os.getenv("MONGO_URI", "")
    owner_jid: str = os.getenv("OWNER_ID","")
    timezone: str = os.getenv("TZ", "Asia/Kolkata")
    whatsapp_enbled:bool = os.getenv("WHATSAPP_ENABLED", "false").lower() in {"1", "true", "yes"}
    session_dir: str = os.getenv("SESSION_DIR", "session")

setings = Settings()
