import json
from rejson import Client, Path
import time
from brokers_api.historical_data import fetch_historical_data

def get_redis_client(host="localhost", port=6379, db=0):
    return Client(host=host, port=port, db=db, decode_responses=True)

def ensure_structure(r, data_type):
    base_path = ".data_streams.candle_data.historical"
    if r.jsonget("trading_setup", Path(f"{base_path}.{data_type}")) is None:
        r.jsonset("trading_setup", Path(f"{base_path}.{data_type}"), [])

def get_instrument_key_by_short_name(r, short_name):
    stocks = r.jsonget("trading_setup", Path(".instruments.instrument_stocks")) or []
    for stock in stocks:
        if stock.get("short_name") == short_name:
            return stock.get("instrument_key")
    return None

def get_underlying_key(r, underlying_symbol):
    options = r.jsonget("trading_setup", Path(".instruments.instrument_options")) or []
    for opt in options:
        if opt.get("underlying_symbol") == underlying_symbol:
            return opt.get("underlying_key")
    return None

def get_missing_instruments(r, active_list, fetched_list, data_type):
    fetched_instruments = {item["instrument"] for item in fetched_list or []}
    missing = []
    
    for item in active_list or []:
        if data_type == "stocks":
            short_name = item.get("short_name")
            if not short_name:
                continue
            instrument_key = get_instrument_key_by_short_name(r, short_name)
            if not instrument_key:
                print(f"[Historiucal] No instrument_key found for short_name: {short_name}")
                continue
            if instrument_key not in fetched_instruments:
                missing.append(instrument_key)
        elif data_type == "options":
            underlying_symbol = item.get("underlying_symbol")
            if not underlying_symbol:
                continue
            underlying_key = get_underlying_key(r, underlying_symbol)
            if not underlying_key:
                print(f"[Historical] No instrument key found for underlying_symbol: {underlying_symbol}")
                continue
            if underlying_key not in fetched_instruments:
                missing.append(underlying_key)
    
    return missing

def update_historical_data(data_type="stocks", redis_host="localhost", redis_port=6379, redis_db=0):
    r = get_redis_client(redis_host, redis_port, redis_db)
    ensure_structure(r, data_type)
    
    active_path = f".instruments.active_{data_type}"
    fetched_path = f".data_streams.candle_data.historical.{data_type}"
    
    active_instruments = r.jsonget("trading_setup", Path(active_path))
    fetched_data = r.jsonget("trading_setup", Path(fetched_path))
    
    if not active_instruments:
        print(f"[Historiucal] No active {data_type} found in Redis.")
        return
    
    to_fetch = get_missing_instruments(r, active_instruments, fetched_data, data_type)
    if not to_fetch:
        # print(f"All {data_type} already up-to-date.")
        return
    
    print(f"Fetching historical data for {len(to_fetch)} {data_type}...")
    for instrument in to_fetch:
        try:
            candle_data = fetch_historical_data(instrument)
            if candle_data:
                entry = {"instrument": instrument, "candles": candle_data}
                r.execute_command("JSON.ARRAPPEND", "trading_setup", fetched_path, json.dumps(entry))
                print(f"Stored {len(candle_data)} candles for {data_type[:-1]} {instrument}")
            else:
                print(f"No candle data returned for {data_type[:-1]} {instrument}")
        except Exception as e:
            print(f"Error fetching data for {instrument}: {e}")
        time.sleep(1.5)

def process_historical_candles():

    update_historical_data("stocks")
    update_historical_data("options")

if __name__ == "__main__":
    print("Starting historical data update...")
    process_historical_candles()