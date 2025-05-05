# --- START OF FILE main.py ---

import threading
import time
import sys
from rejson import Client

# Import functions from your modules (assuming they now accept redis_client)
from utils.redis_setup import initialize_redis
from candle_data.process_candle_data import process_candle_data
from utils.instrument_keys import process_instruments
from brokers_api.start_websocket import start_websocket
from utils.test import websocket_test 
from brokers_api.login import fetch_access_token
from indicators.process_indicators import process_indicators

if __name__ == "__main__":
    print("\nInitializing Redis data structure...")
    redis_client = Client(host="localhost", port=6379, db=0, password=None, decode_responses=True)
    try:
        redis_client.ping()
        print("Redis connection successful.")
    except Exception as e:
        sys.exit(f"Failed to connect to Redis: {e}. Exiting.")
    print("Redis initialization process finished.")
    time.sleep(2)

    # print("\nFetching access token...")
    # fetch_access_token(redis_client)
    # print("Access token fetch process finished.")
    # time.sleep(5)

    # print("\nFetching and processing instruments...")
    # process_instruments(redis_client)
    # print("Instruments fetched and updated.")
    # time.sleep(5)

    print("\nStarting WebSocket thread...")
    websocket_thread = threading.Thread(target=websocket_test, args=(redis_client,))
    websocket_thread.daemon = True
    websocket_thread.start()
    print("Started WebSocket Thread")
    time.sleep(5)

    # print("\nStarting Candle Data processing thread...")
    # candle_data_thread = threading.Thread(target=process_candle_data, args=(redis_client,))
    # candle_data_thread.daemon = True
    # candle_data_thread.start()
    # print("Started Candle Data Thread")
    # time.sleep(5)

    # print("\nStarting Indicators processing thread...")
    # indicators_thread = threading.Thread(target=process_indicators, args=(redis_client,))
    # indicators_thread.daemon = True
    # indicators_thread.start()
    # print("Started Indicators Thread")
    # time.sleep(5)

    # print("\nMain script initialization complete. Background threads running.")
    # print("Press Ctrl+C to exit.")
    # try:
    #     while True:
    #         time.sleep(60)
    #         # Optional: Add health checks for threads here if needed
    #         # e.g., if not websocket_thread.is_alive(): break
    #
    # except KeyboardInterrupt:
    #     print("\nCtrl+C received. Shutting down main script.")
    #
    # print("Main script finished.")

    print("\nMain script initialization complete. WebSocket thread running.")
    print("Press Ctrl+C to exit.")
    try:
        while True:
            websocket_thread.join(60)  # Check every 60 seconds
            if not websocket_thread.is_alive():
                print("ERROR: WebSocket thread stopped unexpectedly.")
                break
    except KeyboardInterrupt:
        print("\nCtrl+C received. Shutting down main script.")
    finally:
        print("Main script finished.")

# --- END OF FILE main.py ---