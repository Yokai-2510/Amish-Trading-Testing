# --- START OF FILE utils/test3.py ---

import upstox_client
from rejson import Client, Path
import sys

# --- Configuration ---
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_PASSWORD = None

# --- Redis Paths ---
TOKEN_PATH = Path(".global_config.credentials.access_token")
ACTIVE_STOCKS_PATH = Path(".instrument_master.active_instruments.stocks")
ACTIVE_OPTIONS_PATH = Path(".instrument_master.active_instruments.options")

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
    stock_keys, option_keys = set(), set()
    try:
        active_stock_configs = redis_client.jsonget("trading_setup", ACTIVE_STOCKS_PATH) or []
        active_option_configs = redis_client.jsonget("trading_setup", ACTIVE_OPTIONS_PATH) or []

        stock_keys = {s['instrument_key'] for s in active_stock_configs if isinstance(s, dict) and 'instrument_key' in s}
        option_keys = {o['underlying_key'] for o in active_option_configs if isinstance(o, dict) and 'underlying_key' in o}

        print(f"DEBUG [websocket]: Found {len(stock_keys)} stocks, {len(option_keys)} option underlyings.")
        return stock_keys | option_keys
    except Exception as e:
        print(f"ERROR [websocket]: get_active_instruments failed: {e}", file=sys.stderr)
        return set()

def websocket_test(redis_client):
    # Initialize Redis client
    
    # Get access token
    access_token = get_access_token(redis_client)
    if not access_token:
        print("ERROR [websocket]: Failed to get access token. Exiting.", file=sys.stderr)
        return
    print(f"Connecting with token: {access_token[:10]}...")

    # Get instruments
    all_keys = get_active_instruments(redis_client)
    if not all_keys:
        print("ERROR [websocket]: No instruments to subscribe. Exiting.", file=sys.stderr)
        return

    # Set up Upstox configuration
    configuration = upstox_client.Configuration()
    configuration.access_token = access_token

    # Initialize WebSocket streamer
    streamer = upstox_client.MarketDataStreamerV3(upstox_client.ApiClient(configuration))

    # Define callbacks
    def on_open():
        print(f"INFO [websocket]: Subscribing to {len(all_keys)} instruments.")
        streamer.subscribe(list(all_keys), "full")
        print("INFO [websocket]: WebSocket connected.")

    def on_message(message):
        print(f"Received: {message}")

    def on_error(error):
        print(f"ERROR [websocket]: WebSocket error: {error}", file=sys.stderr)

    def on_close(ws=None, code=None, reason=None):
        print(f"INFO [websocket]: WebSocket disconnected: Code: {code}, Reason: {reason or 'N/A'}")

    # Assign callbacks
    streamer.on("open", on_open)
    streamer.on("message", on_message)
    streamer.on("error", on_error)
    streamer.on("close", on_close)

    # Connect to WebSocket
    print("INFO [websocket]: Connecting streamer...")
    streamer.connect()

if __name__ == "__main__":
    websocket_test()

# --- END OF FILE utils/test3.py ---