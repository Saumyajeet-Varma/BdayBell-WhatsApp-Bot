from datetime import date
from typing import Any

HELP_TEXT = (
    "*BDayBell Bot Commands* \n\n"
    "*!add [Name] [DD-MM]* - Add a birthday (e.g., !add Saumyajeet-Varma 10-08)\n"
    "*!list* - View all saved birthdays\n"
    "*!ping* - Check if the bot is running\n"
    "*!getid* - Get the ID of the current chat/group\n"
    "*!doc* - Show this help menu"
)

def validate_dd_mm(value: str) -> bool:
    try:
        day, month = map(int, value.split("-"))
        date(2000, month, day)
        return len(value) == 5 and value[2] == "-"
    except (ValueError, TypeError):
        return False

def parse_add_command(text: str) -> tuple[str, str] | None:
    parts = text.strip().split()
    if len(parts) < 3 or parts[0] != "!add":
        return None
    birthday = parts[-1]
    name = " ".join(parts[1:-1]).strip()
    if not name or not validate_dd_mm(birthday):
        return None
    return name, birthday

def format_birthdays(items: list[dict[str, Any]]) -> str:
    if not items:
        return "No birthdays saved yet"
    lines = ["*Saved Birthdays*", ""]
    lines.extend(f"- {item['name']}: {item['date']}" for item in items)
    return "\n".join(lines)

def names_for_reminder(items: list[dict[str, Any]]) -> str:
    names = [str(item["name"]) for item in items]
    if len(names) == 1:
        return names[0]
    if len(names) == 2:
        return f"{names[0]} and {names[1]}"
    return ", ".join(names[:-1]) + f" and {names[-1]}"
