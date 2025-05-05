# --- START OF FILE redis_setup.py (Modified) ---

import json
import os
from rejson import Client, Path

# --- Configuration ---
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_PASSWORD = None
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE_DIR = os.path.join(BASE_DIR, "source")
CREDENTIALS_FILE = os.path.join(SOURCE_DIR, "credentials.json")
FLAGS_FILE = os.path.join(SOURCE_DIR, "flags.json")
OPTIONS_STRATEGY_FILE = os.path.join(SOURCE_DIR, "strategy_options.json")
STOCKS_STRATEGY_FILE = os.path.join(SOURCE_DIR, "strategy_stocks.json")
# Set to True to flush the DB on initialization, False otherwise
FORCE_DB_FLUSH = True # Use with caution, especially on DB 0

# --- Helper Functions ---

def load_json(file_path):
    """Loads JSON data from a file."""
    if not os.path.exists(file_path):
        print(f"Warning: Configuration file not found - {file_path}")
        return None
    try:
        with open(file_path, "r", encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"Warning: Error decoding JSON from {file_path}: {e}")
        return None
    except Exception as e:
        print(f"Warning: Error loading {file_path}: {e}")
        return None

def setup_redis_connection():
    """Establishes connection to the Redis server."""
    try:
        client = Client(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PASSWORD, decode_responses=True)
        client.ping()
        print(f"Connected to Redis at {REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}")
        return client
    except Exception as e:
        print(f"FATAL: Redis connection failed: {e}")
        return None

# --- Initialization Functions ---

def initialize_database(client, force_flush=False):
    """Initializes the database, optionally flushing it first."""
    if force_flush:
        try:
            client.flushdb()
            print(f"Database {REDIS_DB} flushed.")
        except Exception as e:
            print(f"Error flushing database {REDIS_DB}: {e}")
            return False # Stop if flush fails? Decide based on need.
    try:
        # Check if root exists, create if not
        if not client.exists("trading_setup"):
            client.jsonset("trading_setup", Path.rootPath(), {})
            print("Root key 'trading_setup' created.")
        else:
            print("Root key 'trading_setup' already exists.")
        return True
    except Exception as e:
        print(f"Error initializing root key 'trading_setup': {e}")
        return False

def setup_global_config(client):
    """Sets up the .global_config section."""
    print("Setting up '.global_config'...")
    try:
        credentials_data = load_json(CREDENTIALS_FILE) or {}
        flags_data = load_json(FLAGS_FILE) or {}
        path = Path(".global_config")
        # Use JSONSET with XX to update if exists, NX maybe risky if structure changes
        client.jsonset("trading_setup", path, {"credentials": credentials_data, "flags": flags_data})
        print("  '.global_config' set successfully.")
        return True
    except Exception as e:
        print(f"  Error setting '.global_config': {e}")
        return False

def setup_instrument_master(client):
    """Sets up the initial structure for .instrument_master."""
    print("Setting up '.instrument_master'...")
    try:
        instrument_master_structure = {
            "stocks": None, # To be populated by instrument_keys.py
            "options": None, # To be populated by instrument_keys.py
            "active_instruments": {"stocks": [], "options": []} # Populated later in this script
        }
        path = Path(".instrument_master")
        # Set only if it doesn't exist to avoid overwriting populated data later?
        # Or just set it - assuming this runs before instrument_keys
        client.jsonset("trading_setup", path, instrument_master_structure)
        print("  '.instrument_master' structure initialized.")
        return True
    except Exception as e:
        print(f"  Error setting '.instrument_master': {e}")
        return False

def setup_data_streams(client):
    """Sets up the initial structure for .data_streams."""
    print("Setting up '.data_streams'...")
    try:
        data_streams_structure = {
            "instruments_data": {
                "stocks": {},
                "option_chain": {},
                "option_indexes": {}
            },
            "candles": {
                "historical": {"stocks": {}, "options": {}},
                "intraday": {"stocks": {}, "options": {}},
                "websocket": {"stocks": {}, "options": {}} # Populated by websocket handler
            },
            "complete_candles": { # Maybe populated by candle processing module
                "stocks": {},
                "options": {}
            }
        }
        path = Path(".data_streams")
        client.jsonset("trading_setup", path, data_streams_structure)
        print("  '.data_streams' structure initialized.")
        return True
    except Exception as e:
        print(f"  Error setting '.data_streams': {e}")
        return False

def _initialize_single_set_structure():
    """Returns the default structure for a single strategy set status/data."""
    return {
        "active_instruments": [], # Currently selected instruments for this set
        "calculated_indicators": {"entry": {}, "exit": {}},
        "status": {
            "set_operational_status": "inactive", # e.g., inactive, active, paused, error
            "position_status": {}, # Keyed by instrument_key e.g. "NONE", "LONG", "SHORT" (or just "ENTERED" for options?)
            "entry_signal_active": {}, # Keyed by instrument_key: boolean
            "exit_signal_active": {}, # Keyed by instrument_key: boolean
            "current_position_details": {}, # Keyed by instrument_key: { entry_price, timestamp, etc. }
            "calculated_stop_loss_level": {}, # Keyed by instrument_key: float/None
            "calculated_target_profit_level": {}, # Keyed by instrument_key: float/None
            "current_instrument_ltp": {}, # Keyed by instrument_key: float
            "unrealized_pnl": {}, # Keyed by instrument_key: float
            "realized_pnl_today": 0.0,
            "trades_today_count": 0,
            "risk_limits_status": {"max_daily_loss_hit": False, "max_daily_trades_hit": False},
            "last_update_timestamp": None
        },
        "trades": [] # List of executed trades for this set
    }

def setup_sets(client):
    """Sets up the .sets structure based on strategy JSON files."""
    print("Setting up '.sets'...")
    try:
        # Initialize base paths
        client.jsonset("trading_setup", Path(".sets"), {})
        client.jsonset("trading_setup", Path(".sets.stocks"), {})
        client.jsonset("trading_setup", Path(".sets.options"), {})
        print("  Initialized base '.sets' structure.")

        # Process Option Strategies
        all_options_strategies = load_json(OPTIONS_STRATEGY_FILE) or {}
        print(f"  Processing {len(all_options_strategies)} option strategies from file...")
        options_sets_count = 0
        for set_id, set_data in all_options_strategies.items():
            config_data = set_data.get("config")
            indicators_definitions = set_data.get("indicators")
            if not config_data or not indicators_definitions:
                print(f"  Skipping option set '{set_id}': Missing 'config' or 'indicators' section.")
                continue
            try:
                set_path = Path(f".sets.options.{set_id}")
                client.jsonset("trading_setup", set_path, {
                    "config": config_data,
                    "indicators_config": indicators_definitions,
                    **_initialize_single_set_structure() # Add status/data structure
                })
                options_sets_count += 1
            except Exception as e:
                 print(f"  Error setting option set '{set_id}': {e}")
        print(f"  Successfully set up {options_sets_count} option sets.")


        # Process Stock Strategies
        all_stocks_strategies = load_json(STOCKS_STRATEGY_FILE) or {}
        print(f"  Processing {len(all_stocks_strategies)} stock strategies from file...")
        stock_sets_count = 0
        for set_id, set_data in all_stocks_strategies.items():
            config_data = set_data.get("config")
            indicators_definitions = set_data.get("indicators")
            if not config_data or not indicators_definitions:
                print(f"  Skipping stock set '{set_id}': Missing 'config' or 'indicators' section.")
                continue
            try:
                set_path = Path(f".sets.stocks.{set_id}")
                client.jsonset("trading_setup", set_path, {
                    "config": config_data,
                    "indicators_config": indicators_definitions,
                    **_initialize_single_set_structure() # Add status/data structure
                })
                stock_sets_count += 1
            except Exception as e:
                 print(f"  Error setting stock set '{set_id}': {e}")
        print(f"  Successfully set up {stock_sets_count} stock sets.")

        print("  '.sets' setup complete.")
        return True
    except Exception as e:
        print(f"  Error setting up '.sets': {e}")
        return False

def populate_active_strategy_instruments(client):
    """Populates .instrument_master.active_instruments based on active sets."""
    print("Populating '.instrument_master.active_instruments'...")
    active_stock_list = []
    active_option_underlying_list = [] # List of dicts {symbol, key, expiry}
    active_stock_keys = set()          # To avoid duplicate stock instrument keys
    active_underlying_keys = set()     # To avoid duplicate underlying keys (handles only first expiry found per underlying)

    # Process Stock Strategies for Active Instruments
    all_stocks_strategies = load_json(STOCKS_STRATEGY_FILE) or {}
    print(f"  Checking {len(all_stocks_strategies)} stock strategies for active instruments...")
    for set_id, set_data in all_stocks_strategies.items():
        config = set_data.get("config", {})
        # Check if the set itself is active
        if config.get("set_config", {}).get("set_active_status"):
            stocks_config = config.get("stocks_config", {})
            stocks_list = stocks_config.get("stocks", [])
            for stock_info in stocks_list:
                 # Ensure stock_info is a dict and has needed keys
                if isinstance(stock_info, dict):
                    inst_key = stock_info.get("instrument_key")
                    short_name = stock_info.get("short_name")
                    if inst_key and short_name and inst_key not in active_stock_keys:
                        active_stock_keys.add(inst_key)
                        active_stock_list.append({
                            "short_name": short_name,
                            "instrument_key": inst_key
                        })
                else:
                     print(f"  Warning: Invalid stock entry format in set '{set_id}': {stock_info}")

    # Process Option Strategies for Active Instruments
    all_options_strategies = load_json(OPTIONS_STRATEGY_FILE) or {}
    print(f"  Checking {len(all_options_strategies)} option strategies for active instruments...")
    for set_id, set_data in all_options_strategies.items():
        config = set_data.get("config", {})
        # Check if the set itself is active
        if config.get("set_config", {}).get("set_active_status"):
            instrument_config = config.get("instrument_config", {})
            underlying_symbol = instrument_config.get("underlying_symbol")
            underlying_key = instrument_config.get("underlying_key")
            # *** Get the expiry date from the config ***
            expiry_date = instrument_config.get("expiry")

            # Check if required info exists and underlying hasn't been added yet
            if underlying_symbol and underlying_key and expiry_date and underlying_key not in active_underlying_keys:
                active_underlying_keys.add(underlying_key)
                active_option_underlying_list.append({
                    "underlying_symbol": underlying_symbol,
                    "underlying_key": underlying_key,
                    "expiry": expiry_date # *** Add expiry here ***
                })
            elif underlying_key in active_underlying_keys:
                 # Optional: Log if another strategy uses same underlying but different expiry
                 # print(f"  Info: Underlying '{underlying_key}' already added by another active strategy. Skipping for set '{set_id}'.")
                 pass
            elif not expiry_date and underlying_symbol and underlying_key:
                 print(f"  Warning: Active option set '{set_id}' for underlying '{underlying_key}' is missing the 'expiry' date in instrument_config. Skipping.")


    # Save the lists to Redis
    try:
        client.jsonset("trading_setup", Path(".instrument_master.active_instruments.stocks"), active_stock_list)
        print(f"  Set '.instrument_master.active_instruments.stocks' with {len(active_stock_list)} unique stocks.")
        client.jsonset("trading_setup", Path(".instrument_master.active_instruments.options"), active_option_underlying_list)
        print(f"  Set '.instrument_master.active_instruments.options' with {len(active_option_underlying_list)} unique underlying/expiry pairs.")
        print("  Population of '.instrument_master.active_instruments' complete.")
        return True
    except Exception as e:
        print(f"  Error setting active instruments in Redis: {e}")
        return False

def setup_system_logs(client):
    """Sets up the .system_logs section."""
    print("Setting up '.system_logs'...")
    try:
        client.jsonset("trading_setup", Path(".system_logs"), {"connections": [], "global_errors": []})
        print("  '.system_logs' structure initialized.")
        return True
    except Exception as e:
        print(f"  Error setting '.system_logs': {e}")
        return False

# --- Main Initialization Function ---

def initialize_redis():
    """Performs the complete Redis database initialization and setup."""
    print("\n--- Starting Redis Initialization ---")
    client = setup_redis_connection()
    if not client:
        return None # Cannot proceed without connection

    if not initialize_database(client, FORCE_DB_FLUSH):
        return None # Cannot proceed if DB init fails

    # Setup individual sections
    steps = [
        ("Global Config", setup_global_config),
        ("Instrument Master Structure", setup_instrument_master),
        ("Data Streams Structure", setup_data_streams),
        ("Strategy Sets", setup_sets),
        ("System Logs", setup_system_logs),
        # Populate active instruments *after* base structures are set
        ("Populate Active Instruments", populate_active_strategy_instruments),
    ]

    all_successful = True
    for name, func in steps:
        print(f"\n--- Running Step: {name} ---")
        if not func(client):
            print(f"--- Step Failed: {name} ---")
            all_successful = False
            # Decide whether to stop on first failure or continue
            # break # Uncomment to stop on first failure

    print(f"\n--- Redis Initialization {'Completed Successfully' if all_successful else 'Finished with Errors'} ---")
    return client if all_successful else None # Return client only if all steps passed, or adjust as needed

# --- Standalone Execution ---
if __name__ == "__main__":
    initialize_redis()
    print("\nRedis setup script finished.")