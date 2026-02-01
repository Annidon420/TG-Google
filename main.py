import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, CallbackQueryHandler, filters
import requests
from bs4 import BeautifulSoup

def search_text(query):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    results = []
    import time
    for b in range(1, 21, 10):  # b=1,11 for 2 pages
        try:
            response = requests.get(f'https://search.yahoo.com/search?p={query}&b={b}', headers=headers, timeout=10)
            if response.status_code != 200:
                break
            soup = BeautifulSoup(response.text, 'html.parser')
            for algo in soup.find_all('div', class_='algo'):
                h3 = algo.find('h3', class_='title')
                a = algo.find('a')
                p = algo.find('p', class_='fz-ms')
                if h3 and a and 'href' in a.attrs:
                    title = h3.text.strip()
                    link = a['href']
                    snippet = p.text.strip() if p else ""
                    results.append({'title': title, 'link': link, 'snippet': snippet})
            time.sleep(0.5)
            if len(results) >= 50:
                break
        except:
            break
    return results[:50]

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if message.text:
        query = message.text.strip()
        if query:
            results = search_text(query)
            if results:
                keyboard = [
                    [InlineKeyboardButton("Images", callback_data=f"images_{query}"),
                     InlineKeyboardButton("Videos", callback_data=f"videos_{query}")],
                    [InlineKeyboardButton("News", callback_data=f"news_{query}"),
                     InlineKeyboardButton("Maps", callback_data=f"maps_{query}")]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                for i in range(0, len(results), 10):
                    batch = results[i:i+10]
                    response = '\n'.join([f"<b>{r['title']}</b>\n{r['snippet']}\n{r['link']}" for r in batch])
                    await message.reply_text(response, reply_markup=reply_markup if i == 0 else None, parse_mode='HTML')
            else:
                await message.reply_text("No results found.")
        else:
            await message.reply_text("Please send a search query.")

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    if data.startswith("images_"):
        q = data[7:]
        image_url = f"https://duckduckgo.com/?q={q}&iax=images&ia=images"
        response = f"Image search for '{q}': {image_url}"
        await query.edit_message_text(response)
    elif data.startswith("videos_"):
        q = data[7:]
        video_url = f"https://duckduckgo.com/?q={q}&iax=videos&ia=videos"
        response = f"Video search for '{q}': {video_url}"
        await query.edit_message_text(response)
    elif data.startswith("news_"):
        q = data[5:]
        news_url = f"https://duckduckgo.com/?q={q}&iar=news&ia=news"
        response = f"News search for '{q}': {news_url}"
        await query.edit_message_text(response)
    elif data.startswith("maps_"):
        q = data[5:]
        maps_url = f"https://duckduckgo.com/?q={q}&iaxm=maps"
        response = f"Maps search for '{q}': {maps_url}"
        await query.edit_message_text(response)

def main():
    token = "8533376904:AAFnP7-uHk3pbmNDcrPcMIyTp-IE-yONW4k"  # Your bot token
    if not token:
        print("Please set your bot token in the code.")
        return

    application = ApplicationBuilder().token(token).build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(CallbackQueryHandler(handle_callback))
    application.run_polling()

if __name__ == '__main__':
    main()