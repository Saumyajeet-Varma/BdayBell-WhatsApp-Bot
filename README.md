# 🔔 BdayBell — Never Miss a Birthday!

**BdayBell** is a WhatsApp birthday reminder bot built with Python, FastAPI, and MongoDB. It helps you keep track of birthdays, manage birthday records through simple commands, and receive automatic reminders so you never forget to wish someone on their special day.

## ✨ Features

- 🎂 **Birthday Management** — Add and list birthdays using simple WhatsApp commands.
- 🔔 **Automated Reminders** — Receive birthday reminders daily at 10:00 PM for birthdays occurring the following day.
- 💾 **MongoDB Integration** — Persist birthday records in MongoDB.
- ⚡ **FastAPI Backend** — Lightweight HTTP server with health-check endpoints.
- 🌏 **Timezone Support** — Configure the timezone for scheduled reminders.
- 🤖 **WhatsApp Integration** — Connect to WhatsApp through an experimental Python WhatsApp Web client.
- 🩺 **Health Checks** — Monitor application availability through HTTP endpoints.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| FastAPI | HTTP API and application lifecycle |
| PyMongo | MongoDB integration |
| APScheduler | Scheduled birthday reminders |
| WAeys | Experimental WhatsApp Web integration |
| pytest | Automated testing |
| python-dotenv | Environment variable management |

## 📁 Project Structure

```text
BdayBell/
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI application
│   ├── config.py         # Environment configuration
│   ├── database.py       # MongoDB connection
│   ├── birthdays.py      # Birthday validation and formatting
│   ├── commands.py       # WhatsApp command handlers
│   ├── scheduler.py      # Scheduled birthday reminders
│   └── whatsapp.py       # WhatsApp client adapter
├── tests/
│   ├── test_api.py
│   ├── test_birthdays.py
│   └── test_scheduler.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## 🚀 Getting Started

### Prerequisites

- Python 3.11 or later
- A running MongoDB instance or MongoDB Atlas cluster
- A WhatsApp account for linking the bot
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/Saumyajeet-Varma/BdayBell-WhatsApp-Bot
cd BdayBell-WhatsApp-Bot
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it according to your terminal.

**Windows PowerShell**
```powershell
.\.venv\Scripts\Activate.ps1
```

**Git Bash**
```bash
source .venv/Scripts/activate
```

**Linux/macOS**
```bash
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file from `.env.example`.

```env
PORT=3000
MONGO_URI=mongodb://localhost:27017/bdaybell
OWNER_JID=911234567890@s.whatsapp.net
TZ=Asia/Kolkata
WHATSAPP_ENABLED=false
SESSION_DIR=session
```

Update the values for your environment.

| Variable | Description |
|---|---|
| `PORT` | HTTP server port |
| `MONGO_URI` | MongoDB connection string |
| `OWNER_JID` | WhatsApp recipient JID for reminders |
| `TZ` | Timezone used by the reminder scheduler |
| `WHATSAPP_ENABLED` | Enables or disables the WhatsApp client |
| `SESSION_DIR` | Directory for WhatsApp session data |

**Security:** Never commit your `.env` file, MongoDB credentials, or WhatsApp session files to Git.

### 5. Start the Application

```bash
uvicorn app.main:app --host 0.0.0.0 --port 3000
```

The application will be available at:

- API health check: `http://localhost:3000/ping`
- Application status: `http://localhost:3000/health`
- Interactive API documentation: `http://localhost:3000/docs`

The application requires a working MongoDB connection during startup.

## 💬 WhatsApp Commands

Once the WhatsApp client is connected, the bot supports the following commands.

| Command | Description | Example |
|---|---|---|
| `!add [Name] [DD-MM]` | Add a birthday | `!add Saumyajeet 10-08` |
| `!list` | Display saved birthdays | `!list` |
| `!ping` | Check whether the bot is responsive | `!ping` |
| `!getid` | Display the current chat ID | `!getid` |
| `!doc` | Display the command help menu | `!doc` |

### Adding a Birthday

```text
!add Saumyajeet 10-09
```

Example response:

```text
✅ Added Saumyajeet on 10-08
```

### Listing Birthdays

```text
!list
```

Example response:

```text
🎂 Saved Birthdays 🎂

- Aman: 10-08
- Ayush: 11-12
```

### Automated Reminders

BdayBell checks for birthdays occurring the next day and schedules a reminder at **10:00 PM in the configured timezone**.

For example, if someone's birthday is on 10 August, the reminder is scheduled for 09 August at 10:00 PM.

## 🗄️ Database Structure

Birthday information is stored in the MongoDB `birthdays` collection.

Example document:

```json
{
  "name": "Saumyajeet",
  "date": "10-08"
}
```

The date uses the `DD-MM` format. The collection also has an index on the `date` field to support birthday lookups.

## 🧪 Running Tests

Run the automated test suite using:

```bash
pytest -q
```

The tests cover:

- Birthday date validation
- Add-command parsing
- Birthday-list formatting
- Reminder name formatting
- Timezone-aware date calculations
- The `/ping` endpoint response

The current tests do not require a live WhatsApp connection. Database integration and real WhatsApp behavior require separate integration tests.

## ⚠️ WhatsApp Integration Status

The WhatsApp integration uses **WAeys**, an unofficial Python WhatsApp Web client.

This integration is experimental and should not be considered production-ready without compatibility testing.

- WhatsApp may change its protocol and break the integration.
- Existing Baileys authentication sessions are not guaranteed to be compatible.
- Session persistence and message-event handling must be verified against the installed WAeys version.
- The current implementation uses local session storage; persistent storage is required for deployments where the filesystem is ephemeral.

Test pairing, incoming and outgoing messages, application restarts, and scheduled reminders before relying on the bot.

## 🔒 Security and Deployment

- Keep secrets in environment variables.
- Add `session/` and `.env` to `.gitignore`.
- Use a persistent volume for WhatsApp session data.
- Restrict access to API documentation if deploying publicly.
- Configure monitoring and error logging before production use.
- Avoid running multiple scheduler instances against the same bot unless duplicate reminders are prevented.

## 🗺️ Future Improvements

- [ ] Interactive birthday management
- [ ] Edit and delete birthday commands
- [ ] Birthday reminders with customizable times
- [ ] MongoDB-backed WhatsApp session persistence
- [ ] Duplicate-birthday detection
- [ ] Improved logging and error handling
- [ ] Integration tests using a test MongoDB database
- [ ] Reliable WhatsApp reconnection handling
- [ ] Docker-based deployment

## 🤝 Contributing

Contributions and suggestions are welcome!

1. Fork the repository.
2. Create a feature branch.
3. Implement your changes and add tests.
4. Open a pull request describing the changes.

## 📄 License

Add the license that applies to this project. If you intend to distribute it publicly, include a `LICENSE` file in the repository.

---

**BdayBell — A little reminder that makes someone's day.** 🎂🔔