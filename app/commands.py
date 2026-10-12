from app.birthdays import HELP_TEXT, format_birthdays, parse_add_command

INVALID_ADD = "Invalid command format. Use: !add [Name] [DD-MM]"
INVALID_DATE = "Invalid date format. Use DD-MM (e.g., 10-08)."

class CommandHandler:
    def __init__(self, collection, whatsapp_client):
        self.connection = collection
        self.whatsapp = whatsapp_client

    async def handle(self, text: str, chat_jid: str) -> None:
        text = text.strip()
        if text == "!ping":
            await self.whatsapp.send_text(chat_jid, "Heyy!! Bot is awake")
        elif text == "!getid":
            await self.whatsapp.send_text(chat_jid, f"This chat's ID is: {chat_jid}")
        elif text == "!doc":
            await self.whatsapp.send_text(chat_jid, HELP_TEXT)
        elif text.startswith("!add "):
            parts = text.split()
            parsed = parse_add_command(text)
            if not parsed:
                if len(parts) < 3:
                    reply = INVALID_ADD
                elif not parts[-1].count("-") == 1:
                    reply = INVALID_DATE
                else:
                    reply = INVALID_DATE if len(parts[-1]) == 5 else INVALID_DATE
                await self.whatsapp.send_text(chat_jid, reply)
                return
            name, birthday = parsed
            self.collection.insert_one({"name": name, "date": birthday})
            await self.whatsapp.send_text(chat_jid, f"Added {name} on {birthday}")
        elif text == "!list":
            birthdays = list(self.collection.find({}, {"name": 1, "date": 1}).sort("date", 1))
            await self.whatsapp.send_text(chat_jid, format_birthdays(birthdays))
