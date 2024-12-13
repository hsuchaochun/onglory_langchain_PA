import time
import relevanceAI.relevanceai_func.func as func
import relevanceAI.relevanceai_func.tg_func as tg_func
from datetime import datetime
from config import config

EXECUTION_MINUTE = 30
SLEEP_INTERVAL = 60

last_run_hour = None

def is_execution_time(current_time, last_run):
    return (current_time.minute == EXECUTION_MINUTE and 
            (last_run is None or current_time.hour != last_run))

while True:
    current_time = datetime.now()
    
    if is_execution_time(current_time, last_run_hour):
        try:
            last_run_hour = current_time.hour
            print(f"Executing at {current_time}")
            func.news_categorize(number=1, interval="HOUR")
        except Exception as e:
            print(e)
            tg_msg = f"RelevanceAI News Categorize Error:\n{e}"
            tg_func.tg_send_msg(config.TG_SYSTEM_ERROR_API_TOKEN, config.TG_SYSTEM_ERROR_API_GROUP, tg_msg)
            time.sleep(0.2)
            continue
    
    time.sleep(SLEEP_INTERVAL)