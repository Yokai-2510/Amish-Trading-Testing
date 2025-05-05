import time 
from candle_data.dynamic_historical_data import process_historical_candles
from candle_data.dynamic_intraday_data import process_intraday_candles
from candle_data.merge_candle_data import merge_candle_data

def process_candle_data():
    print("Starting candle data processing...")
    while True:
        process_historical_candles()  # Fetch historical data (runs once if up-to-date)
        process_intraday_candles()    # Fetch intraday data (updates periodically)
        merge_candle_data() 
        time.sleep(2)  

if __name__ == '__main__':
    
    process_candle_data()