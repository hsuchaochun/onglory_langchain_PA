# end point: open-api/open-flash?size={size}&page={page}&type={type}

# Query parameters:
# "page":1,  //page
# "size":10, //size
# "type":push //important news
# "lang":cn //language cn,en,cht

import requests
import time
import re
from datetime import datetime, timezone, timedelta
import sys
sys.path.append("../../")
import init
import config

cryptopanic_api_key = config.CRYPTOPANIC_API_KEY
onglory_db = init.mydb
onglory_cursor = init.mycursor

while True:
    page = sys.argv[1] if len(sys.argv) > 1 else 1
    kind = "news" # news, media
    filter = "" # (rising|hot|bullish|bearish|important|saved|lol)
    currencies = "" # BTC,ETH
    regions = "en" # Available regions: en (English), de (Deutsch), nl (Dutch), es (Español), fr (Français), it (Italiano), pt (Português), ru (Русский), tr (Türkçe), ar (عربي), cn (中國人), jp (日本), ko (한국인)
    domain = "https://cryptopanic.com//api//free//v1//posts//"
    endpoint = "?auth_token={cryptopanic_api_key}&kind={kind}&page={page}"
    
    for p in range(1, int(page)+1):
        url = domain + endpoint.format(cryptopanic_api_key=cryptopanic_api_key, kind=kind, page=p)
        
        try:
            response = requests.get(url)
            response.raise_for_status()  # Check if the request was successful
            
            try:
                data = response.json().get("results")
            except (ValueError, AttributeError) as e:
                print(f"Error parsing JSON: {e}")
                continue  # Skip this iteration and wait for the next one

            for news in data:
                platform = "cryptopanic"
                related_coins = ""
                related_coins_symbol = ""
                id = ""
                title = ""
                link = ""
                url = ""
                create_time = ""
                
                if news.get("currencies"):
                    related_coins = news.get("currencies")[0].get("title")
                    related_coins_symbol = news.get("currencies")[0].get("symbol")
                if news.get("id"):
                    id = news.get("id")
                if news.get("title"):
                    title = news.get("title")
                    title = re.sub(r'[\U00010000-\U0010FFFF]', '', title)
                if news.get("url"):
                    link = news.get("url")
                if news.get("source"):
                    if news.get("source").get("domain"):
                        url = news.get("source").get("domain")
                if news.get("created_at"):
                    create_time = news.get("created_at")
                    # Convert to a datetime object (assuming it's UTC)
                    datetime_obj = datetime.strptime(create_time, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)
                    # Define the UTC+8 timezone
                    timezone_utc_plus_8 = timezone(timedelta(hours=8))
                    # Convert to the desired timezone (UTC+8)
                    create_time_str = datetime_obj.astimezone(timezone_utc_plus_8).strftime('%Y-%m-%d %H:%M:%S')
                    
                # content = news.get("")
                # pic = news.get("")

                # print(f"ID: {id}, \nTitle: {title}, \nRelated Coins: {related_coins}, \nRelated Coins Symbol: {related_coins_symbol}, \nLink: {link}, \nURL: {url}, \nCreate Time: {create_time}")
                # print()
                
                # Check if the news exists
                sql = "SELECT * FROM news WHERE id = %s and platform = %s"
                val = (id, platform)
                onglory_cursor.execute(sql, val)
                result = onglory_cursor.fetchall()
                if len(result) == 0:
                    print(f"News ID: {id}, Title: {title}, Create Time: {create_time_str}")
                    # Insert the news
                    sql = "INSERT INTO news (id, title, related_coins, related_coins_symbol, link, url, create_time, platform) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                    val = (id, title, related_coins, related_coins_symbol, link, url, create_time_str, platform)
                    try:
                        onglory_cursor.execute(sql, val)
                        onglory_db.commit()
                        # print(f"News {id} inserted.")
                    except Exception as e:
                        print(f"Insert failed: {e}")
                        continue
                # else:
                #     print(f"News {id} exists.")

        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")

    # Wait for 60 seconds before running the loop again
    time.sleep(60)