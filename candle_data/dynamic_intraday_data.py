import json
from rejson import Client, Path
import time
from brokers_api.intraday_data import fetch_intraday_data

def get_redis_client(host="localhost", port=6379, db=0):
    """Create and return a Redis client."""
    return Client(host=host, port=port, db=db, decode_responses=True)

def ensure_structure(r, data_type):
    """Ensure the intraday data structure exists in Redis."""
    base_path = ".data_streams.candle_data.intraday"
    if r.jsonget("trading_setup", Path(f"{base_path}.{data_type}")) is None:
        r.jsonset("trading_setup", Path(f"{base_path}.{data_type}"), [])
        # print(f"Initialized empty intraday {data_type} list in Redis.")

def get_instrument_key_by_short_name(r, short_name):
    """Retrieve the instrument_key for a given short_name from instrument_stocks."""
    stocks = r.jsonget("trading_setup", Path(".instruments.instrument_stocks")) or []
    for stock in stocks:
        if stock.get("short_name") == short_name:
            return stock.get("instrument_key")
    return None

def get_underlying_key(r, underlying_symbol):
    """Retrieve the underlying_key for a given underlying_symbol from instrument_options."""
    options = r.jsonget("trading_setup", Path(".instruments.instrument_options")) or []
    for opt in options:
        if opt.get("underlying_symbol") == underlying_symbol:
            return opt.get("underlying_key")
    return None

def get_missing_instruments(r, active_list, fetched_list, data_type):
    """Identify active instruments that lack intraday data."""
    fetched_instruments = {item["instrument"] for item in fetched_list or []}
    missing = []
    
    for item in active_list or []:
        if data_type == "stocks":
            short_name = item.get("short_name")
            if not short_name:
                continue
            instrument_key = get_instrument_key_by_short_name(r, short_name)
            if not instrument_key:
                # print(f"[Intraday] No instrument_key found for short_name: {short_name}")
                continue
            if instrument_key not in fetched_instruments:
                missing.append(instrument_key)
        elif data_type == "options":
            underlying_symbol = item.get("underlying_symbol")
            if not underlying_symbol:
                continue
            underlying_key = get_underlying_key(r, underlying_symbol)
            if not underlying_key:
                # print(f"[Intraday] No underlying_key found for underlying_symbol: {underlying_symbol}")
                continue
            if underlying_key not in fetched_instruments:
                missing.append(underlying_key)
    
    return missing

def update_intraday_data(data_type="stocks", redis_host="localhost", redis_port=6379, redis_db=0):
    """Fetch and store intraday candle data for missing instruments."""
    r = get_redis_client(redis_host, redis_port, redis_db)
    ensure_structure(r, data_type)
    
    active_path = f".instruments.active_{data_type}"
    fetched_path = f".data_streams.candle_data.intraday.{data_type}"
    
    active_instruments = r.jsonget("trading_setup", Path(active_path))
    fetched_data = r.jsonget("trading_setup", Path(fetched_path))
    
    if not active_instruments:
        print(f"No active {data_type} found in Redis.")
        return
    
    to_fetch = get_missing_instruments(r, active_instruments, fetched_data, data_type)
    if not to_fetch:
        # print(f"All {data_type} already up-to-date.")
        return
    
    # print(f"Fetching intraday data for {len(to_fetch)} {data_type}...")
    for instrument in to_fetch:
        try:
            candle_data = fetch_intraday_data(instrument)
            if candle_data:
                entry = {"instrument": instrument, "candles": candle_data}
                r.execute_command("JSON.ARRAPPEND", "trading_setup", fetched_path, json.dumps(entry))
                # print(f"Stored {len(candle_data)} candles for {data_type[:-1]} {instrument}")
            # else:
            #     print(f"[Intraday] No candle data returned for {data_type[:-1]} {instrument}")
        except Exception as e:
            print(f"Error fetching intraday data for {instrument}: {e}")
        time.sleep(2)  # Small delay to respect API rate limits

def process_intraday_candles():
    """Process intraday candle data for both stocks and options."""
    # print("Updating intraday data for stocks...")
    update_intraday_data("stocks")
    # print("\nUpdating intraday data for options...")
    update_intraday_data("options")
    # print("Intraday data update complete.")

if __name__ == "__main__":
    print("Starting intraday data update...")
    process_intraday_candles()