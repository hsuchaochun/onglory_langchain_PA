import time
import relevanceai_func.func as func
import relevanceai_func.tg_func as tg_func
from datetime import datetime
from config import config

EXECUTION_HOUR = 8
EXECUTION_MINUTE = 5
SLEEP_INTERVAL = 60  # seconds

last_run_date = None

def is_execution_time(current_time, last_run):
    return (current_time.hour == EXECUTION_HOUR and 
            current_time.minute == EXECUTION_MINUTE and 
            current_time.date() != last_run)

while True:
    current_time = datetime.now()
    
    if is_execution_time(current_time, last_run_date):
        try:
            last_run_date = current_time.date()
            func.create_and_send_daily_summary()
            print(f"Daily summary successfully triggered at {current_time}")
        except Exception as e:
            print(e)
            tg_msg = f"RelevanceAI Daily Summary Error:\n{e}"
            tg_func.tg_send_msg(config.TG_SYSTEM_ERROR_API_TOKEN, config.TG_SYSTEM_ERROR_API_GROUP, tg_msg)
            time.sleep(0.2)
            continue
    
    time.sleep(SLEEP_INTERVAL)