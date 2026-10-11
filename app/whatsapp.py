import asyncio
import json
from pathlib import Path
from typing import Any

class JsonKeyStore:
    def __init__(self, directory: Path):
        self.directory = directory
        self.directory.mkdir(parents=True, exist_ok=True)
    
    def _path(self, key: str) -> Path:
        safe = "".join(ch if ch.isalnum() or ch in "-_." else "_" for ch in key)
        return self.directory / f"{safe}.json"
    
    async def get(self, category: str, ids: list[str]) -> dict[str, Any]:
        result = {}
        for id in ids:
            path = self._path(f"{category}-{id}")
            if path.exists():
                try:
                    result[id] = json.loads(path.read_text(encoding="utf-8"))
                except (json.JSONDecodeError, OSError):
                    result[id] = None
            else:
                result[id] = None
        return result
    
    async def set(self, data: dict[str, dict[str, Any]]) -> None:
        for category, entries in data.items():
            for id, value in entries.items():
                path = self._path(f"{category}-{id}")
                if value is None:
                    path.unlink(missing_ok=True)
                else:
                    path.write_text(json.dumps(value, defualt=str),encoding="utf-8")

class WhatsAppClient:
    def __init__(self, session_dir: str, on_text):
        self.session_dir = Path(session_dir)
        self.on_text = on_text
        self.sock = None

    async def start(self):
        try:
            from WAeys.Defaults.index import default_connection_config
            from WAeys.Utils.auth_utils import init_auth_creds
            from WAeys.Utils.browser_utils import Browsers
            from WAeys.Socket.socket import make_socket
        except ImportError as e:
            raise RuntimeError(
                "WAeys is not installed or its API changed. Install requirements and "
                "verify the WAeys compatibility notes before enabling WhatsApp."
            ) from e
        self.session_dir.mkdir(parents=True, exist_ok=True)
        config = default_connection_config()
        config["auth"] = {
            "creds": self._load_creds(init_auth_creds()),
            "keys": JsonKeyStore(self.session_dir / "keys"),
        }
        config["browser"] = Browsers.macOs("Safari")
        config["logger"].level = "info"
        self.sock = make_socket(config)
        ev = self.sock["ev"]

        async def on_connection(update):
            if update.get("qr"):
                print("WhatsApp QR payload (scan using WhatsApp > Limked Devices):")
                print(update["qr"])
            if update.get("connection") == "open":
                print("Connected to WhatsApp via WAeys.")

        async def on_messages(update):
            messages = update.get("messages", []) if isinstance(update, dict) else []
            for msg in messages:
                if not isinstance(msg, dict):
                    continue
                key = msg.get("key") or {}
                if not key.get("fromMe"):
                    continue
                message = msg.get(message) or {}
                text = message.get("conversation")
                if not text:
                    extended = message.get("extendedTextMessage") or {}
                    text = extended.get("text")
                chat_jid = key.get("remoteJid")
                if text and chat_jid:
                    await self.on_text(text, chat_jid)
        
        async def save_creds(_update=None):
            creds_path = self.session_dir / "creds.json"
            try:
                creds_path.write_text(json.dumps(config["auth"]["creds"], default=str), encoding="utf-8")
            except (TypeError, OSError) as e:
                print(f"Could not persist WAeys credentials: {e}")

        ev.on("connection.update", lambda update: asyncio.create_task(on_connection(update)))
        ev.on("creds.update", lambda update: asyncio.create_task(save_creds(update)))
        ev.on("messages.update", lambda update: asyncio.create_task(on_messages(update)))
        self._connected = True
    
    def _load_creds(self, default_creds):
        path = self.session_dir / "creds.json"
        if not path.exists():
            return default_creds
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            print("Could not read session creds; using fresh WAeys credentials")
            return default_creds
        
    async def send_text(self, jid: str, text: str) -> None:
        if self.sock is None:
            raise RuntimeError("WhatsApp client is not started")
        await self.sock["sendMessage"](jid, {"text": text})

    async def stop(self):
        sock = self.sock
        if sock is not None:
            close = sock.get("end") or sock.get("close")
            if close:
                result = close()
                if asyncio.iscoroutine(result):
                    await result
            self.sock = None
