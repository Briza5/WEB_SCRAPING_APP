# Event Scraper & Notifier

An automated Python tool that monitors a tour website for new events. When a new event is detected, it stores the data in an SQLite database and sends an email notification.

## 🌟 Features
- **Web Scraping:** Fetches live data using the `requests` library.
- **Data Extraction:** Uses `selectorlib` with YAML templates for clean data parsing.
- **Database Persistence:** Uses `SQLite` to track seen events and prevent duplicate notifications.
- **Email Alerts:** Sends automated emails via Gmail SMTP with STARTTLS encryption.
- **Security:** Sensitive credentials (email password) are managed via environment variables.

## 🛠️ Installation

1. Clone this repository to your local machine.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
Ensure you have an extract.yml file in the root directory with the correct CSS selectors.

🔑 Configuration
Before running the script, set up your Gmail App Password as an environment variable:

Windows (PowerShell):

PowerShell

$env:PYTHON_EMAILING_PASSWORD = "your_app_password_here"
macOS / Linux:

Bash

export PYTHON_EMAILING_PASSWORD="your_app_password_here"
🚀 Usage
Run the main script to start monitoring:

Bash

python main.py
The script will check the website every 2 seconds. If a new tour is found that isn't already in data.db, you will receive an email.

📁 Project Structure
main.py: The core logic (scraping, database, main loop).

send_email.py: Module for handling secure email delivery.

extract.yml: Configuration file for CSS selectors.

data.db: SQLite database (created automatically on first run).