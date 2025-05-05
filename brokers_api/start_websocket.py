# --- START OF FILE brokers_api/start_websocket.py ---

import upstox_client
from rejson import Client, Path
import threading
import time
import sys

# --- Configuration ---
MONITOR_INTERVAL = 15
RECONNECT_INTERVAL = 10
RECONNECT_RETRY_COUNT = 30

# --- Redis Paths ---
TOKEN_PATH = Path(".global_config.credentials.access_token")
ACTIVE_STOCKS_PATH = Path(".instrument_master.active_instruments.stocks")
ACTIVE_OPTIONS_PATH = Path(".instrument_master.active_instruments.options")
MASTER_STOCKS_PATH = Path(".instrument_master.stocks")
MASTER_OPTIONS_PATH = Path(".instrument_master.options")
LIVE_STOCKS_PATH = Path(".data_streams.instruments_data.stocks")
LIVE_INDEXES_PATH = Path(".data_streams.instruments_data.option_indexes")
LIVE_OPTION_CHAIN_PATH = Path(".data_streams.instruments_data.option_chain")
WS_STOCK_CANDLES_PATH = Path(".data_streams.candles.websocket.stocks")
WS_INDEX_CANDLES_PATH = Path(".data_streams.candles.websocket.options")

# --- Core Functions ---
def get_access_token(redis_client):
    try:
        token = redis_client.jsonget("trading_setup", TOKEN_PATH)
        if not token:
            print("ERROR [websocket]: Access token not found.", file=sys.stderr)
            return None
        return token.strip()
    except Exception as e:
        print(f"ERROR [websocket]: get_access_token failed: {e}", file=sys.stderr)
        return None

def get_active_instruments(redis_client):
    print("DEBUG [websocket]: Fetching active instruments...")
    active_stock_keys, index_keys, option_keys = set(), set(), set()
    master_stocks, index_map, option_map = {}, {}, {}
    master_options_groups = {}
    try:
        active_stock_configs = redis_client.jsonget("trading_setup", ACTIVE_STOCKS_PATH) or []
        active_option_configs = redis_client.jsonget("trading_setup", ACTIVE_OPTIONS_PATH) or []
        all_master_stocks = redis_client.jsonget("trading_setup", MASTER_STOCKS_PATH) or []
        all_master_options = redis_client.jsonget("trading_setup", MASTER_OPTIONS_PATH) or []

        active_stock_keys = {s['instrument_key'] for s in active_stock_configs if isinstance(s, dict) and 'instrument_key' in s}
        for stock_data in all_master_stocks:
            if isinstance(stock_data, dict) and stock_data.get('instrument_key') in active_stock_keys:
                master_stocks[stock_data['instrument_key']] = stock_data

        active_underlying_info = {
            opt_conf['underlying_key']: opt_conf['expiry']
            for opt_conf in active_option_configs
            if isinstance(opt_conf, dict) and 'underlying_key' in opt_conf and 'expiry' in opt_conf
        }
        active_underlying_keys = set(active_underlying_info.keys())

        for group in all_master_options:
            if not isinstance(group, dict): continue
            underlying_key = group.get('underlying_key')
            if underlying_key in active_underlying_keys:
                master_options_groups[underlying_key] = group
                index_keys.add(underlying_key)
                index_map[underlying_key] = {"instrument_key": underlying_key, "underlying_symbol": group.get("underlying_symbol", "N/A")}
                target_expiry = active_underlying_info[underlying_key]
                for contract in group.get('options', []):
                    if not isinstance(contract, dict): continue
                    instrument_key = contract.get('instrument_key')
                    if instrument_key and contract.get('expiry_formatted') == target_expiry:
                        option_keys.add(instrument_key)
                        option_map[instrument_key] = {**contract, "underlying_key": underlying_key, "underlying_symbol": group.get("underlying_symbol", "N/A")}

        print(f"DEBUG [websocket]: Found {len(active_stock_keys)} stocks, {len(index_keys)} indices, {len(option_keys)} options.")
        return active_stock_keys, index_keys, option_keys, master_stocks, index_map, option_map, master_options_groups
    except Exception as e:
        print(f"ERROR [websocket]: get_active_instruments failed: {e}", file=sys.stderr)
        return set(), set(), set(), {}, {}, {}, {}

def process_websocket_message(redis_client, message, subscribed_stock_keys, subscribed_index_keys, subscribed_option_keys, master_stocks_map, master_indexes_map, master_options_map, master_options_groups_map):
    feeds = message.get("feeds", {})
    if not feeds:
        return

    try:
        current_stocks = redis_client.jsonget("trading_setup", LIVE_STOCKS_PATH) or {}
        current_indexes = redis_client.jsonget("trading_setup", LIVE_INDEXES_PATH) or {}
        current_option_chain = redis_client.jsonget("trading_setup", LIVE_OPTION_CHAIN_PATH) or {}
        stock_candles = redis_client.jsonget("trading_setup", WS_STOCK_CANDLES_PATH) or {}
        index_candles = redis_client.jsonget("trading_setup", WS_INDEX_CANDLES_PATH) or {}
        updated = False

        for instrument_key, feed_data in feeds.items():
            ff_data = feed_data.get("ff", {})
            live_feed = ff_data.get("marketFF", ff_data.get("indexFF", {}))
            ohlc_feed = ff_data.get("marketOHLC", {}).get("ohlc", [])
            ltpc_data = ff_data.get("ltpc", {})

            if not isinstance(live_feed, dict):
                live_feed = {}

            if instrument_key in subscribed_stock_keys:
                master_data = master_stocks_map.get(instrument_key)
                if master_data:
                    stock_entry = {**master_data}
                    if ltpc_data.get('ltp') is not None:
                        live_feed['ltp'] = ltpc_data['ltp']
                    stock_entry["live_data"] = live_feed
                    current_stocks[instrument_key] = stock_entry
                    updated = True
                    filtered_ohlc = [c for c in ohlc_feed if c.get("interval") in ["I1", "1d"]]
                    if filtered_ohlc:
                        stock_candles[instrument_key] = {
                            "instrument_key": instrument_key,
                            "short_name": master_data.get("short_name", "N/A"),
                            "ohlc": filtered_ohlc
                        }

            elif instrument_key in subscribed_index_keys:
                master_data = master_indexes_map.get(instrument_key)
                if master_data:
                    index_entry = {**master_data}
                    if ltpc_data.get('ltp') is not None:
                        live_feed['ltp'] = ltpc_data['ltp']
                    index_entry["live_data"] = live_feed
                    current_indexes[instrument_key] = index_entry
                    updated = True
                    filtered_ohlc = [c for c in ohlc_feed if c.get("interval") in ["I1", "1d"]]
                    if filtered_ohlc:
                        index_candles[instrument_key] = {
                            "instrument_key": instrument_key,
                            "underlying_symbol": master_data.get("underlying_symbol", "N/A"),
                            "ohlc": filtered_ohlc
                        }

            elif instrument_key in subscribed_option_keys:
                master_data = master_options_map.get(instrument_key)
                if master_data:
                    underlying_key = master_data.get("underlying_key")
                    underlying_symbol = master_data.get("underlying_symbol")
                    if not underlying_key or not underlying_symbol:
                        continue
                    master_chain_group = master_options_groups_map.get(underlying_key)
                    if not master_chain_group:
                        continue

                    if underlying_symbol not in current_option_chain:
                        current_option_chain[underlying_symbol] = {"index_name": underlying_symbol, "option_chain": []}

                    found_contract = False
                    for contract_entry in current_option_chain[underlying_symbol]["option_chain"]:
                        if isinstance(contract_entry, dict) and contract_entry.get("instrument_key") == instrument_key:
                            if ltpc_data.get('ltp') is not None:
                                live_feed['ltp'] = ltpc_data['ltp']
                            contract_entry["live_data"] = live_feed
                            found_contract = True
                            updated = True
                            break

                    if not found_contract:
                        new_contract_entry = {**master_data}
                        if ltpc_data.get('ltp') is not None:
                            live_feed['ltp'] = ltpc_data['ltp']
                        new_contract_entry["live_data"] = live_feed
                        current_option_chain[underlying_symbol]["option_chain"].append(new_contract_entry)
                        updated = True

        if updated:
            redis_client.jsonset("trading_setup", LIVE_STOCKS_PATH, current_stocks)
            redis_client.jsonset("trading_setup", LIVE_INDEXES_PATH, current_indexes)
            redis_client.jsonset("trading_setup", LIVE_OPTION_CHAIN_PATH, current_option_chain)
            redis_client.jsonset("trading_setup", WS_STOCK_CANDLES_PATH, stock_candles)
            redis_client.jsonset("trading_setup", WS_INDEX_CANDLES_PATH, index_candles)

    except Exception as e:
        print(f"ERROR [websocket]: process_websocket_message failed: {e}", file=sys.stderr)

def monitor_instruments(redis_client, streamer, shared_data, stop_event):
    print("INFO [websocket]: Starting instrument monitor thread.")
    while not stop_event.is_set():
        try:
            if not streamer:
                print("DEBUG [monitor]: Streamer not initialized. Waiting...")
                time.sleep(MONITOR_INTERVAL)
                continue

            print("DEBUG [monitor]: Checking instrument changes...")
            new_s_keys, new_i_keys, new_o_keys, new_s_map, new_i_map, new_o_map, new_og_map = get_active_instruments(redis_client)

            shared_data['subscribed_stock_keys'] = new_s_keys
            shared_data['subscribed_index_keys'] = new_i_keys
            shared_data['subscribed_option_keys'] = new_o_keys
            shared_data['master_stocks_map'] = new_s_map
            shared_data['master_indexes_map'] = new_i_map
            shared_data['master_options_map'] = new_o_map
            shared_data['master_options_groups_map'] = new_og_map

            current_subscriptions = shared_data.get('current_server_subscriptions', set())
            new_all_keys = new_s_keys | new_i_keys | new_o_keys

            to_unsubscribe = current_subscriptions - new_all_keys
            to_subscribe = new_all_keys - current_subscriptions

            if streamer.is_connected():
                if to_unsubscribe:
                    print(f"INFO [monitor]: Unsubscribing from {len(to_unsubscribe)} instruments.")
                    streamer.unsubscribe(list(to_unsubscribe))
                    current_subscriptions.difference_update(to_unsubscribe)
                if to_subscribe:
                    print(f"INFO [monitor]: Subscribing to {len(to_subscribe)} instruments.")
                    streamer.subscribe(list(to_subscribe), "full")
                    current_subscriptions.update(to_subscribe)
                shared_data['current_server_subscriptions'] = current_subscriptions
            else:
                print("DEBUG [monitor]: WebSocket not connected, skipping subscribe/unsubscribe.")

        except Exception as e:
            print(f"ERROR [monitor]: Monitor loop failed: {e}", file=sys.stderr)

        stop_event.wait(MONITOR_INTERVAL)
    print("INFO [websocket]: Monitor thread stopped.")

def start_websocket(redis_client):
    print("INFO [websocket]: Starting WebSocket...")
    stop_event = threading.Event()
    shared_data = {
        'subscribed_stock_keys': set(),
        'subscribed_index_keys': set(),
        'subscribed_option_keys': set(),
        'master_stocks_map': {},
        'master_indexes_map': {},
        'master_options_map': {},
        'master_options_groups_map': {},
        'current_server_subscriptions': set()
    }

    # Initial instrument load
    print("INFO [websocket]: Loading active instruments...")
    s_keys, i_keys, o_keys, s_map, i_map, o_map, og_map = get_active_instruments(redis_client)
    shared_data['subscribed_stock_keys'] = s_keys
    shared_data['subscribed_index_keys'] = i_keys
    shared_data['subscribed_option_keys'] = o_keys
    shared_data['master_stocks_map'] = s_map
    shared_data['master_indexes_map'] = i_map
    shared_data['master_options_map'] = o_map
    shared_data['master_options_groups_map'] = og_map
    if not (s_keys or i_keys or o_keys):
        print("ERROR [websocket]: No instruments loaded. Exiting.", file=sys.stderr)
        return

    # Start monitor thread
    monitor_thread = threading.Thread(target=monitor_instruments, args=(redis_client, None, shared_data, stop_event), daemon=True)
    monitor_thread.start()

    while not stop_event.is_set():
        access_token = get_access_token(redis_client)
        if not access_token:
            print(f"WARN [websocket]: No access token. Retrying in {RECONNECT_INTERVAL}s...")
            time.sleep(RECONNECT_INTERVAL)
            continue

        print(f"INFO [websocket]: Attempting connection with token: {access_token[:10]}...")
        try:
            config = upstox_client.Configuration()
            config.access_token = access_token
            streamer = upstox_client.MarketDataStreamerV3(upstox_client.ApiClient(config))

            def on_open():
                all_keys = (shared_data['subscribed_stock_keys'] |
                            shared_data['subscribed_index_keys'] |
                            shared_data['subscribed_option_keys'])
                if all_keys:
                    print(f"INFO [websocket]: Subscribing to {len(all_keys)} instruments.")
                    streamer.subscribe(list(all_keys), "full")
                    shared_data['current_server_subscriptions'] = all_keys.copy()
                else:
                    print("WARN [websocket]: No instruments to subscribe.")
                print("INFO [websocket]: WebSocket connected.")

            def on_message(message):
                process_websocket_message(redis_client, message,
                                         shared_data['subscribed_stock_keys'],
                                         shared_data['subscribed_index_keys'],
                                         shared_data['subscribed_option_keys'],
                                         shared_data['master_stocks_map'],
                                         shared_data['master_indexes_map'],
                                         shared_data['master_options_map'],
                                         shared_data['master_options_groups_map'])

            def on_error(error):
                print(f"ERROR [websocket]: WebSocket error: {error}", file=sys.stderr)

            def on_close(ws=None, code=None, reason=None):
                shared_data['current_server_subscriptions'] = set()
                print(f"INFO [websocket]: WebSocket disconnected: Code: {code}, Reason: {reason or 'N/A'}")

            streamer.on("open", on_open)
            streamer.on("message", on_message)
            streamer.on("error", on_error)
            streamer.on("close", on_close)

            streamer.auto_reconnect(enable=True, interval=RECONNECT_INTERVAL, retry_count=RECONNECT_RETRY_COUNT)
            print("INFO [websocket]: Connecting streamer...")
            streamer.connect()

        except upstox_client.exceptions.ApiException as api_e:
            print(f"ERROR [websocket]: API Exception: {api_e.status} - {api_e.reason}", file=sys.stderr)
            if api_e.status in (401, 403):
                print("ERROR [websocket]: Authentication error (401/403). Waiting before retry.")
        except Exception as e:
            print(f"ERROR [websocket]: Connection error: {e}", file=sys.stderr)

        if 'streamer' in locals():
            try:
                streamer.disconnect()
            except Exception:
                pass
        time.sleep(RECONNECT_INTERVAL)

    stop_event.set()
    monitor_thread.join(timeout=5)
    print("INFO [websocket]: WebSocket stopped.")

# --- Standalone Execution ---
if __name__ == "__main__":
    print("--- Running start_websocket.py directly ---")
    redis_client = Client(host="localhost", port=6379, db=0, password=None, decode_responses=True)
    try:
        redis_client.ping()
    except Exception as e:
        sys.exit(f"FATAL [websocket]: Redis connection failed: {e}")
    start_websocket(redis_client)
    print("--- start_websocket.py finished ---")

# --- END OF FILE brokers_api/start_websocket.py ---