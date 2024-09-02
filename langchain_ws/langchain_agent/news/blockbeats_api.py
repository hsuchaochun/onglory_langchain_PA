# end point: open-api/open-flash?size={size}&page={page}&type={type}

# Query parameters:
# "page":1,  //page
# "size":10, //size
# "type":push //important news
# "lang":cn //language cn,en,cht

import requests
import time
from datetime import datetime
import sys
sys.path.append("../../")
import init

onglory_db = init.mydb
onglory_cursor = init.mycursor

while True:
    page = 1
    size = sys.argv[1] if len(sys.argv) > 1 else 10
    type = "" # 'push': important news
    # lang = "cht" # 'cn': Chinese, 'en': English, 'cht': Traditional Chinese
    domain = "https://api.theblockbeats.news/v1/"
    endpoint = "open-api/open-flash?size={size}&page={page}&type={type}"
    url = domain + endpoint.format(size=size, page=page, type=type)
    
    try:
        response = requests.get(url)
        # print(response.json())
        response.raise_for_status()  # Check if the request was successful
        
        if response.json().get("status") != 0:
            print(f"Error: {response.get('msg')}")
            continue
        
        try:
            data = response.json().get("data").get("data")
        except (ValueError, AttributeError) as e:
            print(f"Error parsing JSON: {e}")
            continue  # Skip this iteration and wait for the next one

        for news in data:
            platform = "blockbeats"
            id = ""
            title = ""
            content = ""
            pic = ""
            link = ""
            url = ""
            create_time_str = ""
            
            if news.get("id"):
                id = news.get("id")
            if news.get("title"):
                title = news.get("title")
            if news.get("content"):
                content = news.get("content")
                content = content.replace("<p>", "").replace("</p>", "").replace("<br>", "").replace("</br>", "")
            if news.get("pic"):
                pic = news.get("pic")
            if news.get("link"):
                link = news.get("link")
            if news.get("url"):
                url = news.get("url")
            if news.get("create_time"):
                create_time = news.get("create_time")
                create_time_str = datetime.fromtimestamp(int(create_time)).strftime('%Y-%m-%d %H:%M:%S')

            # Check if the news exists
            sql = "SELECT * FROM news WHERE id = %s"
            val = (id, )
            onglory_cursor.execute(sql, val)
            result = onglory_cursor.fetchall()
            if len(result) == 0:
                print(f"News ID: {id}, Title: {title}, Create Time: {create_time_str}")
                # Insert the news
                sql = "INSERT INTO news (platform, id, title, content, pic, link, url, create_time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                val = (platform, id, title, content, pic, link, url, create_time_str)
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