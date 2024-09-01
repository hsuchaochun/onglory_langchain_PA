# end point: open-api/open-flash?size={size}&page={page}&type={type}

# Query parameters:
# "page":1,  //page
# "size":10, //size
# "type":push //important news
# "lang":cn //language cn,en,cht

import requests
import datetime
import time
import sys
sys.path.append("../../")
import init

onglory_db = init.mydb
onglory_cursor = init.mycursor

while True:
    page = 1
    size = 10
    type = "" # 'push': important news
    # lang = "cht" # 'cn': Chinese, 'en': English, 'cht': Traditional Chinese
    domain = "https://api.theblockbeats.news/v1/"
    endpoint = "open-api/open-flash?size={size}&page={page}&type={type}"
    url = domain + endpoint.format(size=size, page=page, type=type)
    
    try:
        response = requests.get(url)
        print(response.json())
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
            id = news.get("id")
            title = news.get("title")
            content = news.get("content")
            content = content.replace("<p>", "").replace("</p>", "").replace("<br>", "").replace("</br>", "")
            pic = news.get("pic")
            link = news.get("link")
            url = news.get("url")
            create_time = news.get("create_time")
            create_time_str = datetime.datetime.fromtimestamp(int(create_time)).strftime('%Y-%m-%d %H:%M:%S')

            # Check if the news exists
            sql = "SELECT * FROM news WHERE id = %s"
            val = (id, )
            onglory_cursor.execute(sql, val)
            result = onglory_cursor.fetchall()
            if len(result) == 0:
                # Insert the news
                sql = "INSERT INTO news (id, title, content, pic, link, url, create_time) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                val = (id, title, content, pic, link, url, create_time_str)
                onglory_cursor.execute(sql, val)
                onglory_db.commit()
                print(f"News {id} inserted.")
            else:
                print(f"News {id} exists.")
                break

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

    # Wait for 60 seconds before running the loop again
    time.sleep(60)