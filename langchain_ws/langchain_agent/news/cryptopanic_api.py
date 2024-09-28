import requests
import time
import re
from datetime import datetime, timezone, timedelta
import sys
import logging
from typing import Dict, Any, List
sys.path.append("../../")
import init
import config

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class CryptoPanicAPI:
    def __init__(self):
        self.api_key = config.CRYPTOPANIC_API_KEY
        self.db = init.mydb
        self.cursor = init.mycursor
        self.base_url = "https://cryptopanic.com/api/free/v1/posts/"
        self.params = {
            "auth_token": self.api_key,
            "kind": "news",
            "page": 1
        }

    def fetch_news(self, page: int) -> List[Dict[str, Any]]:
        self.params["page"] = page
        try:
            response = requests.get(self.base_url, params=self.params)
            response.raise_for_status()
            return response.json().get("results", [])
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed for page {page}: {e}")
            return []

    def parse_news(self, news: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "platform": "cryptopanic",
            "id": news.get("id", ""),
            "title": re.sub(r'[\U00010000-\U0010FFFF]', '', news.get("title", "")),
            "related_coins": news.get("currencies", [{}])[0].get("title", ""),
            "related_coins_symbol": news.get("currencies", [{}])[0].get("symbol", ""),
            "link": news.get("url", ""),
            "url": news.get("source", {}).get("domain", ""),
            "create_time": self.format_time(news.get("published_at", ""))
        }

    @staticmethod
    def format_time(time_str: str) -> str:
        if not time_str:
            return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            dt = datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)
            return dt.astimezone(timezone(timedelta(hours=8))).strftime('%Y-%m-%d %H:%M:%S')
        except ValueError:
            logging.error(f"Invalid datetime format: {time_str}")
            return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def news_exists(self, news_id: str) -> bool:
        self.cursor.execute("SELECT 1 FROM news WHERE id = %s AND platform = %s", (news_id, "cryptopanic"))
        return bool(self.cursor.fetchone())

    def insert_news(self, news: Dict[str, Any]) -> None:
        sql = """
        INSERT INTO news (platform, id, title, related_coins, related_coins_symbol, link, url, create_time)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        try:
            self.cursor.execute(sql, tuple(news.values()))
            self.db.commit()
            logging.info(f"Inserted news: Create time {news['create_time']}, ID {news['id']}, Title: {news['title']}")
        except Exception as e:
            logging.error(f"Insert failed: {e}")

    def run(self, page_size: int):
        while True:
            for page in range(1, page_size + 1):  # Fetch pages 1 to page_size
                news_data = self.fetch_news(page)
                for news_item in news_data:
                    parsed_news = self.parse_news(news_item)
                    if not self.news_exists(parsed_news['id']):
                        self.insert_news(parsed_news)
                time.sleep(1)  # Sleep for 1 seconds between page requests to avoid rate limiting
            time.sleep(60)  # Sleep for 60 seconds after fetching all pages

if __name__ == "__main__":
    page_size = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    api = CryptoPanicAPI()
    api.run(page_size)