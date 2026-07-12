import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import psycopg2
import time

load_dotenv()


DB_CONFIG = f"dbname=chatbot_db user=postgres password={os.getenv('POSTGRES_PASSWORD')} host=localhost"

def save_to_db(url, content):
    conn = psycopg2.connect(DB_CONFIG)
    cur = conn.cursor()
    cur.execute("INSERT INTO knowledge_base (url, content) VALUES (%s, %s) ON CONFLICT (url) DO NOTHING", (url, content))
    conn.commit()
    cur.close()
    conn.close()

def crawl(start_url):
    visited = set()
    queue = [start_url]
    base_domain = urlparse(start_url).netloc

    while queue:
        url = queue.pop(0)
        
        # Skip URLs that are likely to be in a different language or already visited
        path = urlparse(url).path.strip('/')
        parts = path.split('/')
        
        # Check if the first part of the path is a language code (e.g., 'en', 'fr', 'es') or if the URL has already been visited
        is_lang_code = len(parts) > 0 and (len(parts[0]) == 2 or '-' in parts[0])
        
        if is_lang_code or url in visited:
            continue
            
        print(f"Crawling: {url}")
        try:
            response = requests.get(url, timeout=5)
            if response.status_code != 200:
                continue
            
            visited.add(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            main_content = soup.select_one("div.md-content")
            if main_content:
                for tag in main_content.select("nav, footer, script, style, .md-sidebar"):
                    tag.decompose()
                text = main_content.get_text(separator=' ', strip=True)
                save_to_db(url, text)
            
            for link in soup.find_all('a', href=True):
                full_url = urljoin(url, link['href']).split('#')[0]
                if urlparse(full_url).netloc == base_domain and full_url not in visited:
                    queue.append(full_url)
            
            time.sleep(0.5)
        except Exception as e:
            print(f"Error {url}: {e}")

if __name__ == "__main__":
    crawl("https://fastapi.tiangolo.com/")