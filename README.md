# Telegram Google Search Bot

A Telegram bot that allows users to search Google directly from Telegram.

## Features

- Send any text query to the bot
- The bot searches Google and returns top 5 results with titles and links

## Setup Instructions

1. **Create a Telegram Bot:**
   - Message @BotFather on Telegram
   - Use `/newbot` command and follow the instructions
   - Save the bot token

2. **Set Environment Variable:**
   - Set `TELEGRAM_BOT_TOKEN` to your bot token
   - On Windows: `set TELEGRAM_BOT_TOKEN=your_token_here`

3. **Install Dependencies:**
   ```
   pip install -r requirements.txt
   ```

4. **Run the Bot:**
   ```
   python main.py
   ```

## Usage

- Start a chat with the bot
- Send any text message (e.g., "latest news" or "python tutorial")
- The bot will reply with Google search results

## Commands

- Just send text messages to search Google
- No special commands needed; any text is treated as a search query