from rejson import Client, Path
from datetime import datetime
import time 

REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_PASSWORD = None

def get_redis_client():
    return Client(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PASSWORD, decode_responses=True)

def normalize_timestamp(ts):
    if isinstance(ts, (int, float)):
        return datetime.fromtimestamp(ts / 1000).strftime("%Y-%m-%dT%H:%M:%S+05:30")
    elif isinstance(ts, str) and ts.isdigit():
        return datetime.fromtimestamp(int(ts) / 1000).strftime("%Y-%m-%dT%H:%M:%S+05:30")
    return ts or datetime.now().replace(second=0, microsecond=0).strftime("%Y-%m-%dT%H:%M:%S+05:30")

def normalize_candle(candle, source):
    ts = normalize_timestamp(candle.get("ts") if source == "websocket" else candle[0])
    return {
        "timestamp": ts,
        "open": float(candle.get("open", 0) if source == "websocket" else candle[1]),
        "high": float(candle.get("high", 0) if source == "websocket" else candle[2]),
        "low": float(candle.get("low", 0) if source == "websocket" else candle[3]),
        "close": float(candle.get("close", 0) if source == "websocket" else candle[4]),
        "volume": int(candle.get("volume", 0) if source == "websocket" else candle[5])
    }

def initialize_complete_candles(r, data_type):
    historical_path = f".data_streams.candle_data.historical.{data_type}"
    intraday_path = f".data_streams.candle_data.intraday.{data_type}"
    complete_path = f".data_streams.candle_data.complete_candles.{data_type}"

    historical = r.jsonget("trading_setup", Path(historical_path)) or []
    intraday = r.jsonget("trading_setup", Path(intraday_path)) or []
    complete = r.jsonget("trading_setup", Path(complete_path)) or {}

    for entry in historical:
        instrument = entry.get("instrument")
        if instrument and entry.get("candles"):
            complete[instrument] = [normalize_candle(c, "historical") for c in entry["candles"]]

    for entry in intraday:
        instrument = entry.get("instrument")
        if instrument:
            if instrument not in complete:
                complete[instrument] = []
            if entry.get("candles"):
                new_candles = [normalize_candle(c, "intraday") for c in entry["candles"]]
                existing_ts = {c["timestamp"] for c in complete[instrument]}
                complete[instrument].extend(c for c in new_candles if c["timestamp"] not in existing_ts)
                complete[instrument].sort(key=lambda x: x["timestamp"])

    r.jsonset("trading_setup", Path(complete_path), complete)
    print(f"Initialized complete {data_type}: {len(complete)} instruments")

def update_complete_candles(r, data_type, source):
    source_path = f".data_streams.candle_data.{source}.{data_type}" if source == "intraday" else f".data_streams.websocket.candles.{data_type}"
    complete_path = f".data_streams.candle_data.complete_candles.{data_type}"

    source_data = r.jsonget("trading_setup", Path(source_path)) or []
    complete = r.jsonget("trading_setup", Path(complete_path)) or {}

    for entry in source_data:
        instrument = entry.get("instrument") or entry.get("instrument_key")
        if not instrument:
            continue
        if instrument not in complete:
            complete[instrument] = []
        
        new_candles = []
        if source == "intraday" and entry.get("candles"):
            new_candles = [normalize_candle(c, "intraday") for c in entry["candles"]]
        elif source == "websocket" and entry.get("ohlc"):
            new_candles = [normalize_candle(c, "websocket") for c in entry["ohlc"] if c.get("interval") == "I1"]

        if new_candles:
            existing_ts = {c["timestamp"] for c in complete[instrument]}
            if source == "websocket" and complete[instrument]:
                complete[instrument] = [c for c in complete[instrument][:-2] if c["timestamp"] in existing_ts]
            complete[instrument].extend(c for c in new_candles if c["timestamp"] not in existing_ts)
            complete[instrument].sort(key=lambda x: x["timestamp"])

    r.jsonset("trading_setup", Path(complete_path), complete)
    # print(f"Updated complete {data_type} from {source}: {len(complete)} instruments")

def merge_candle_data(initial=True):
    r = get_redis_client()
    if initial:
        # print("Performing initial merge...")
        initialize_complete_candles(r, "stocks")
        initialize_complete_candles(r, "options")
    # else:
    #     # print("Updating with intraday data...")
    #     update_complete_candles(r, "stocks", "intraday")
    #     update_complete_candles(r, "options", "intraday")
    #     update_complete_candles(r, "stocks", "websocket")
    #     update_complete_candles(r, "options", "websocket")

    # time.sleep(1)

if __name__ == "__main__":
    merge_candle_data(initial=True)