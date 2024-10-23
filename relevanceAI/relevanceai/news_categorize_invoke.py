import time
import func
from datetime import datetime

EXECUTION_MINUTE = 30
SLEEP_INTERVAL = 3600

last_run_hour = None

def is_execution_time(current_time, last_run):
    return (current_time.minute == EXECUTION_MINUTE and 
            (last_run is None or current_time.hour != last_run))

while True:
    current_time = datetime.now()
    
    if is_execution_time(current_time, last_run_hour):
        last_run_hour = current_time.hour
        func.news_categorize()
    
    time.sleep(SLEEP_INTERVAL)