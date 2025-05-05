# --- START OF FILE print_banknifty_expiries.py ---

from rejson import Client, Path
import sys
import os
from collections import defaultdict

# --- Configuration ---
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_PASSWORD = None  # Set your password if needed, otherwise leave as None

# The key for BankNifty
TARGET_UNDERLYING_KEY = "NSE_INDEX|Nifty 50"

# Redis Path to Read From
REDIS_OPTIONS_PATH = ".instrument_master.options"

# --- Main Function ---
def print_banknifty_expiries_from_redis():
    """
    Connects to Redis, finds the BankNifty option group, and prints its
    unique expiry timestamps alongside their formatted versions.
    """
    print(f"Connecting to Redis at {REDIS_HOST}:{REDIS_PORT} DB {REDIS_DB}...")
    try:
        redis_client = Client(
            host=REDIS_HOST,
            port=REDIS_PORT,
            db=REDIS_DB,
            password=REDIS_PASSWORD,
            decode_responses=True # Important for getting strings directly
        )
        redis_client.ping()
        print("Redis connection successful.")
    except Exception as e:
        print(f"FATAL: Could not connect to Redis: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"\nFetching option groups from Redis path: '{REDIS_OPTIONS_PATH}'...")
    try:
        # Fetch the entire options master list as an array from Redis
        all_options_master = redis_client.jsonget("trading_setup", Path(REDIS_OPTIONS_PATH))

        if not all_options_master:
            print(f"Error: '{REDIS_OPTIONS_PATH}' not found or is empty in Redis.", file=sys.stderr)
            print("Please ensure 'instrument_keys.py' (with formatting) has run successfully first.")
            sys.exit(1)
        elif not isinstance(all_options_master, list):
             print(f"Error: Data at '{REDIS_OPTIONS_PATH}' is not a list.", file=sys.stderr)
             sys.exit(1)

        # Find the BankNifty group
        banknifty_data = None
        for underlying_group in all_options_master:
            if isinstance(underlying_group, dict) and underlying_group.get("underlying_key") == TARGET_UNDERLYING_KEY:
                banknifty_data = underlying_group
                break # Found it

        if not banknifty_data:
            print(f"Error: Could not find data for underlying key '{TARGET_UNDERLYING_KEY}' in '{REDIS_OPTIONS_PATH}'.", file=sys.stderr)
            sys.exit(1)

        underlying_symbol = banknifty_data.get("underlying_symbol", "N/A")
        print(f"Found data for {TARGET_UNDERLYING_KEY} (Symbol: {underlying_symbol}). Extracting expiries...")

        # Get the list of option contracts associated with this underlying
        option_contracts = banknifty_data.get("options", [])
        if not option_contracts:
            print(f"Warning: No option contracts ('options' array) found listed under '{TARGET_UNDERLYING_KEY}' in Redis.", file=sys.stderr)
            sys.exit(0)

        # Use a dictionary to store unique pairs, keyed by original timestamp for sorting
        unique_expiries = {}
        print(f"Processing {len(option_contracts)} BANKNIFTY contracts...")
        for contract in option_contracts:
             if not isinstance(contract, dict):
                 print(f"  Warning: Skipping item in options list as it's not a dictionary: {contract}", file=sys.stderr)
                 continue

             original_expiry = contract.get('expiry')
             formatted_expiry = contract.get('expiry_formatted', 'N/A') # Get formatted version

             if original_expiry is not None:
                 # Use original_expiry (as number if possible) as the key for uniqueness and sorting
                 try:
                     expiry_key = float(original_expiry) # Convert for reliable comparison/sorting
                     if expiry_key not in unique_expiries:
                         unique_expiries[expiry_key] = {
                             "original": original_expiry, # Store original value (could be string/num)
                             "formatted": formatted_expiry
                         }
                 except (ValueError, TypeError):
                      print(f"  Warning: Could not use original expiry '{original_expiry}' as a numeric key. Skipping this specific entry for sorting.", file=sys.stderr)
                      # Still might want to collect these separately if needed

        if not unique_expiries:
            print("No valid expiry data found in the BankNifty option contracts.", file=sys.stderr)
            sys.exit(0)

        # Sort the collected unique expiries based on the numeric key (original timestamp)
        # items() gives (key, value) pairs, sort by key (item[0])
        sorted_unique_expiries = sorted(unique_expiries.items(), key=lambda item: item[0])

        print(f"\nUnique Expiry Pairs for {TARGET_UNDERLYING_KEY} found in Redis:")
        print("-" * 60)
        print(f"{'Original Timestamp':<20} | {'Formatted (YYYY-MM-DD)':<25}")
        print("-" * 60)
        for _, expiry_data in sorted_unique_expiries:
            original_ts = expiry_data.get('original', 'Error')
            formatted_dt = expiry_data.get('formatted', 'Error')
            print(f"{str(original_ts):<20} | {str(formatted_dt):<25}")
        print("-" * 60)
        print(f"\nFound {len(sorted_unique_expiries)} unique expiries.")

    except Exception as e:
        print(f"\nAn error occurred during processing: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    print_banknifty_expiries_from_redis()

# --- END OF FILE print_banknifty_expiries.py ---