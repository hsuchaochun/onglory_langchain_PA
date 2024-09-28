import requests
import time
from datetime import datetime
import sys
import logging
from typing import Dict, Any, List
sys.path.append("../../")
import init

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class BlockBeatsAPI:
    def __init__(self):
        self.db = init.mydb
        self.cursor = init.mycursor
        self.domain = "https://api.theblockbeats.news/v1/"
        self.endpoint = "open-api/open-flash?size={size}&page={page}&type={type}"

    def fetch_news(self, size: int = 10, page: int = 1, news_type: str = "") -> List[Dict[str, Any]]:
        url = self.domain + self.endpoint.format(size=size, page=page, type=news_type)
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json().get("data", {}).get("data", [])
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e}")
            return []

    def parse_news(self, news_item: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "platform": "blockbeats",
            "id": news_item.get("id", ""),
            "title": news_item.get("title", ""),
            "content": self.clean_content(news_item.get("content", "")),
            "pic": news_item.get("pic", ""),
            "link": news_item.get("link", ""),
            "url": news_item.get("url", ""),
            "create_time": self.format_time(news_item.get("create_time", 0))
        }

    @staticmethod
    def clean_content(content: str) -> str:
        return content.replace("<p>", "").replace("</p>", "").replace("<br>", "").replace("</br>", "")

    @staticmethod
    def format_time(timestamp: int) -> str:
        return datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')

    def insert_news(self, news: Dict[str, Any]) -> None:
        sql = """
        INSERT INTO news (platform, id, title, content, pic, link, url, create_time) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        try:
            self.cursor.execute(sql, tuple(news.values()))
            self.db.commit()
            logging.info(f"Inserted news: Create time {news['create_time']}, ID {news['id']}, Title: {news['title']}")
        except Exception as e:
            logging.error(f"Insert failed: {e}")

    def news_exists(self, news_id: str) -> bool:
        self.cursor.execute("SELECT 1 FROM news WHERE id = %s AND platform = %s", (news_id, "blockbeats"))
        return bool(self.cursor.fetchone())
    
    def run(self, size: int = 10):
        while True:
            news_data = self.fetch_news(size=size)
            for news_item in news_data:
                parsed_news = self.parse_news(news_item)
                if not self.news_exists(parsed_news['id']):
                    self.insert_news(parsed_news)
            time.sleep(60)

if __name__ == "__main__":
    size = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    api = BlockBeatsAPI()
    api.run(size)