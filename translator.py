import aiohttp
import asyncio
import json
import os
import time
from urllib.parse import quote_plus, unquote
from bs4 import BeautifulSoup
import requests
# Cache file path for persistent caching
CACHE_FILE_PATH = 'languages_cache.json'
CACHE_EXPIRY_TIME = 24 * 60 * 60  # 24 hours (in seconds)

# Function to get supported languages from Google Translate page
def google_get_supported_languages():
    # Check if the cache file exists and if it's still valid
    if os.path.exists(CACHE_FILE_PATH):
        with open(CACHE_FILE_PATH, 'r', encoding='utf-8') as f:
            cache_data = json.load(f)
        cache_time = cache_data.get('timestamp', 0)
        if time.time() - cache_time < CACHE_EXPIRY_TIME:
            return cache_data['languages']

    # Fetch languages from the website
    url = "https://cloud.google.com/translate/docs/languages"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the table with the supported languages
    table = soup.find_all('table')[0]
    rows = table.find_all('tr')

    languages = {}
    for row in rows[1:]:
        cols = row.find_all('td')
        if len(cols) >= 2:
            language_name = cols[0].get_text(strip=True)
            iso_code = cols[1].get_text(strip=True)
            languages[iso_code] = language_name

    cache_data = {
        'timestamp': time.time(),
        'languages': languages
    }
    with open(CACHE_FILE_PATH, 'w', encoding='utf-8') as f:
        json.dump(cache_data, f, ensure_ascii=False, indent=4)

    return languages

# Function to check if a language code is valid
def google_is_valid_language_code(language_code, supported_languages=None):
    if supported_languages is None:
        supported_languages = google_get_supported_languages()
    return language_code == "auto" or language_code in supported_languages or language_code in ["zh-CN", "zh-TW"]

# Function to split text into chunks
def split_text(text, chunk_size):
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

# Function to handle translation for a single chunk
async def translate_chunk_async(chunk, target_language, source_language, session):
    formatted_text = quote_plus(chunk)
    formatted_link = f"https://translate.google.com/m?tl={target_language}&sl={source_language}&q={formatted_text}"

    async with session.get(formatted_link) as response:
        if response.status == 200:
            soup = BeautifulSoup(await response.text(), 'html.parser')
            translation = soup.find('div', class_='result-container').get_text(strip=True)
            return unquote(translation)
        else:
            raise ValueError(f"Translation failed for chunk: {chunk}")

async def google_translate_long_text_async(text, target_language="zh-CN", source_language="auto", chunk_size=1000):
    supported_languages = google_get_supported_languages()

    if not google_is_valid_language_code(target_language, supported_languages):
        raise ValueError("Invalid target language code.")

    if not google_is_valid_language_code(source_language, supported_languages):
        raise ValueError("Invalid source language code.")

    text_chunks = split_text(text, chunk_size) if len(text) > chunk_size else [text]

    async with aiohttp.ClientSession() as session:
        tasks = [translate_chunk_async(chunk, target_language, source_language, session) for chunk in text_chunks]
        translations = await asyncio.gather(*tasks)

    return " ".join(translations)
