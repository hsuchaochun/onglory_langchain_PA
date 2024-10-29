import time
import func
from datetime import datetime

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
        last_run_date = current_time.date()
        func.create_and_send_daily_summary()
        print(f"Daily summary successfully triggered at {current_time}")
    
    time.sleep(SLEEP_INTERVAL)