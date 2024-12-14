import time
import requests

def tg_send_msg(api_token, api_group, msg):
    tg_api_url = f"https://api.telegram.org/bot{api_token}/sendMessage?chat_id=@{api_group}&text={msg}"
    
    try:
        tg_resp = requests.get(tg_api_url)
    except Exception as e: 
        print(e)
        time.sleep(0.2)
        tg_resp = requests.get(tg_api_url)

    return tg_resp