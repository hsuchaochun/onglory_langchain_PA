import sys
import time
import threading
from blockbeats_api import BlockBeatsAPI
from cryptopanic_api import CryptoPanicAPI

if __name__ == "__main__":
    blockbeats_page_size = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    cryptopanic_page_size = int(sys.argv[2]) if len(sys.argv) > 1 else 5
    
    blockbeats_api = BlockBeatsAPI()
    cryptopanic_api = CryptoPanicAPI()
    
    stop_event = threading.Event()  # {{ edit_1 }}: Create a stop event for thread management

    def run_api(api, page_size):
        while not stop_event.is_set():  # {{ edit_2 }}: Check the stop event
            api.run(page_size)
            time.sleep(60)  # Sleep for 60 seconds before the next run

    # Create and start threads for each API
    blockbeats_thread = threading.Thread(target=run_api, args=(blockbeats_api, blockbeats_page_size))
    cryptopanic_thread = threading.Thread(target=run_api, args=(cryptopanic_api, cryptopanic_page_size))

    blockbeats_thread.start()
    cryptopanic_thread.start()

    # Keep the main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping the script...")
        stop_event.set()  # {{ edit_3 }}: Signal threads to stop
        blockbeats_thread.join()  # {{ edit_4 }}: Wait for the blockbeats thread to finish
        cryptopanic_thread.join()  # {{ edit_5 }}: Wait for the cryptopanic thread to finish