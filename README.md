# PyReminder

A CLI reminder app with Telegram notifications, built with PostgreSQL, raw SQL, and bot integrations in Python.

## What it does

- Add reminders with a name and due date
- View all stored reminders
- Edit or delete existing reminders
- Sends Telegram alerts for reminders due today and tomorrow

## Usage

```bash
uv run main.py
```

```
Select an option number:
1: Add a Reminder.
2: Show Reminders.
3: Edit Reminders.
4: Quit
```

## Telegram Alerts

Run the checker manually or schedule it to run daily:

```bash
uv run checker.py
```

You'll receive a Telegram message for any reminder due today or tomorrow.

## Setup

**1. Clone the repo and install dependencies**

```bash
git clone https://github.com/anugrahnm/pyreminder
cd pyreminder
uv sync
```

**2. Create a Telegram bot**

- Message [@BotFather](https://t.me/botfather) on Telegram and follow the steps to create a bot
- Copy your bot token

**3. Get your chat ID**

- Message [@userinfobot](https://t.me/userinfobot) on Telegram
- Copy the ID it returns

**4. Create a `.env` file in the project root**

```
TOKEN=your_bot_token
CHAT_ID=your_chat_id
DB_HOST=localhost
DB_PORT=5432
DB_NAME=pyreminder
DB_USER=postgres
DB_PASSWORD=your_password
```

**5. Run**

```bash
uv run main.py       # CLI reminder manager
uv run checker.py    # Send Telegram alerts
```

## Built with

- Python
- PostgreSQL
- psycopg2-binary
- python-telegram-bot
- python-dotenv

## Notes

Originally built with SQLite3, migrated to PostgreSQL.
