# end point: open-api/open-flash?size={size}&page={page}&type={type}

# Query parameters:
# "page":1,  //page
# "size":10, //size
# "type":push //important news
# "lang":cn //language cn,en,cht

import requests
import json
import datetime

page = 1
size = 10
type = "" # 'push': important news
# lang = "cht" # 'cn': Chinese, 'en': English, 'cht': Traditional Chinese
domain = "https://api.theblockbeats.news/v1/"
endpoint = "open-api/open-flash?size={size}&page={page}&type={type}"
url = domain + endpoint.format(size=size, page=page, type=type)

response = requests.get(url)
# print(response.json().get("data").get("data"))
response = response.json().get("data").get("data")
for news in response:
    id = news.get("id")
    title = news.get("title")
    content = news.get("content")
    content = content.replace("<p>", "").replace("</p>", "").replace("<br>", "").replace("</br>", "")
    pic = news.get("pic")
    link = news.get("link")
    url = news.get("url")
    create_time = news.get("create_time")
    create_time_str = datetime.datetime.fromtimestamp(int(create_time)).strftime('%Y-%m-%d %H:%M:%S')
    
    print(f"id: {id}, title: {title}, content: {content}, pic: {pic}, link: {link}, url: {url}, create_time: {create_time_str}")
    print()