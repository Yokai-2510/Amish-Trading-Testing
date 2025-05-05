# --- utils/instrument_keys.py (Refactored + Expiry Formatting) ---

import json
import requests
import gzip
import shutil
import os
import csv
import time
from rejson import Client, Path
from collections import defaultdict
import math  # For checking float validity
from datetime import datetime # For formatting expiry

# --- Constants ---
# File paths (assuming source dir is one level up from this script's dir)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE_DIR = os.path.join(BASE_DIR, "source")
INSTRUMENT_GZ = os.path.join(SOURCE_DIR, "complete.json.gz")
INSTRUMENT_JSON = os.path.join(SOURCE_DIR, "complete.json")
NIFTY_100_CSV = os.path.join(SOURCE_DIR, "ind_nifty100list.csv")

# Download settings
DOWNLOAD_FRESH = False # Set to False to use existing files if present
UPSTOX_URL = "https://assets.upstox.com/market-quote/instruments/exchange/complete.json.gz"
NIFTY_URL = "https://nsearchives.nseindia.com/content/indices/ind_nifty100list.csv" # Verify this URL still works
REQ_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0'
}

# LTP Fetching Settings
LTP_API_URL = "https://api.upstox.com/v2/market-quote/ltp"
LTP_BATCH_SIZE = 500 # Upstox limit might be around 500
DEFAULT_LTP_VALUE = 0.0 # Value to use if LTP fetch fails for an instrument/underlying

# Redis Paths (Keep consistent with existing structure)
REDIS_TOKEN_PATH = ".global_config.credentials.access_token"
REDIS_STOCKS_PATH = ".instrument_master.stocks"
REDIS_OPTIONS_PATH = ".instrument_master.options"

# Option Strike Filtering Settings
FILTER_OPTION_STRIKES = True # Set to False to disable strike filtering
STRIKE_INTERVALS = 10 # Number of strike intervals above/below LTP to keep

# --- Date Formatting ---
DATE_FORMAT = '%Y-%m-%d'
DEFAULT_FORMATTED_DATE = 'N/A'

# --- Main Orchestrator ---

def process_instruments(client):
    """Main orchestrator for instrument processing"""
    start_time = time.time()
    print("\n============================================")
    print("=== Instrument Master Processing Start (Refactored + Expiry Formatting) ===")
    print("============================================")

    if not verify_redis_connection(client):
        return False

    access_token = get_access_token(client)
    if not access_token:
        print("Warning: Access token not found. LTP fetching will be skipped.")
        # Continue without LTP or return False based on requirements

    # --- Stage 1: Acquire and Load Data ---
    raw_instruments, nifty_isins = acquire_and_load_data()
    if raw_instruments is None or nifty_isins is None:
        return False # Exit if data acquisition failed

    # --- Stage 2: Filter Instruments & Group Options ---
    selected_stocks, options_by_underlying, all_keys_for_ltp = \
        filter_and_group_instruments(raw_instruments, nifty_isins)

    # --- Stage 3: Fetch LTPs ---
    ltp_map = {}
    if access_token and all_keys_for_ltp:
        ltp_map = fetch_ltps(all_keys_for_ltp, access_token)
    elif not all_keys_for_ltp:
         print("  No instruments identified for LTP fetching.")
    else: # No access token case
        print("  Skipping LTP fetch due to missing access token.")
        # Populate ltp_map with default values for all keys if proceeding
        ltp_map = {key: DEFAULT_LTP_VALUE for key in all_keys_for_ltp}

    # --- Stage 4: Enrich Data & Final Structure (Includes expiry formatting) ---
    master_stocks, master_options = enrich_and_structure_data(
        selected_stocks, options_by_underlying, ltp_map
    )

    # --- Stage 5: Save to Redis ---
    save_success = save_to_redis(client, master_stocks, master_options)

    # --- Completion ---
    end_time = time.time()
    status = "Successfully" if save_success else "With Errors"
    print(f"\n=== Instrument Master Processing Finished {status} ({end_time - start_time:.2f}s) ===")
    print("============================================")
    return save_success

# --- Helper Functions: Redis ---

def verify_redis_connection(client):
    """Checks if the Redis client is valid and connected."""
    if not client:
        print("Error: Redis client instance required.")
        return False
    try:
        client.ping()
        print("Redis connection verified.")
        return True
    except Exception as e:
        print(f"Redis connection error: {e}")
        return False

def get_access_token(client):
    """Retrieve access token from Redis"""
    try:
        token = client.jsonget("trading_setup", Path(REDIS_TOKEN_PATH))
        if not token:
            print("Warning: Access token not found in Redis.")
            return None
        print("Access token retrieved.")
        return token.strip()
    except Exception as e:
        print(f"Error retrieving access token: {e}")
        return None

def save_to_redis(client, master_stocks, master_options):
    """Save the final master lists to Redis"""
    print("\n--- Stage 5: Saving Master Lists to Redis ---")
    success = True

    try:
        if master_stocks is not None: # Allow saving empty list if needed
            client.jsonset("trading_setup", Path(REDIS_STOCKS_PATH), master_stocks)
            print(f"  Saved {len(master_stocks)} stock records to '{REDIS_STOCKS_PATH}'.")
        else:
            print(f"  Skipping save to '{REDIS_STOCKS_PATH}' (data is None).")
            success = False # Or handle as needed
    except Exception as e:
        print(f"  Error saving to '{REDIS_STOCKS_PATH}': {e}")
        success = False

    try:
        if master_options is not None: # Allow saving empty list
            client.jsonset("trading_setup", Path(REDIS_OPTIONS_PATH), master_options)
            print(f"  Saved {len(master_options)} underlying option groups to '{REDIS_OPTIONS_PATH}'.")
        else:
            print(f"  Skipping save to '{REDIS_OPTIONS_PATH}' (data is None).")
            success = False # Or handle as needed
    except Exception as e:
        print(f"  Error saving to '{REDIS_OPTIONS_PATH}': {e}")
        success = False

    print(f"--- Stage 5 {'Complete' if success else 'Finished with Errors'}: Redis Save Operation ---")
    return success

# --- Helper Functions: Data Acquisition ---

def acquire_and_load_data():
    """Handles file downloads and loading into memory"""
    print("\n--- Stage 1: Acquiring and Loading Data ---")
    os.makedirs(SOURCE_DIR, exist_ok=True)

    # Handle source files
    if DOWNLOAD_FRESH:
        print("  Downloading fresh source files...")
        if not download_file(UPSTOX_URL, INSTRUMENT_GZ, "Upstox instruments", REQ_HEADERS):
            return None, None
        if not extract_gzip(INSTRUMENT_GZ, INSTRUMENT_JSON):
            return None, None
        if not download_file(NIFTY_URL, NIFTY_100_CSV, "Nifty 100 list", REQ_HEADERS):
            print("  Warning: Failed to download Nifty 100 list. Stock filtering may be incomplete.")
            # return None, None # Option to fail hard
        print("  Source file download/extraction complete.")
    else:
        if not os.path.exists(INSTRUMENT_JSON):
             print(f"  Error: Instrument file not found ({INSTRUMENT_JSON}) and DOWNLOAD_FRESH is False.")
             return None, None
        if not os.path.exists(NIFTY_100_CSV):
             print(f"  Warning: Nifty 100 file not found ({NIFTY_100_CSV}) and DOWNLOAD_FRESH is False. Stock filtering incomplete.")
        print("  Using existing source files.")

    # Load data from files
    print("  Loading data from files...")
    instruments, isins = None, set()

    try:
        with open(INSTRUMENT_JSON, 'r', encoding='utf-8') as f:
            instruments = json.load(f)
        print(f"    Loaded instruments JSON ({len(instruments or [])} records).")
    except Exception as e:
        print(f"    Error loading instruments JSON: {e}")
        return None, None # Fail if instruments can't load

    if os.path.exists(NIFTY_100_CSV):
        try:
            with open(NIFTY_100_CSV, 'r', encoding='utf-8') as f_header:
                header = next(csv.reader(f_header), None)
                if header is None:
                    raise ValueError("Nifty 100 CSV is empty or header is missing.")
                try:
                    isin_col_index = header.index('ISIN Code') # Find ISIN column
                except ValueError:
                    print("    Error: 'ISIN Code' column not found in Nifty 100 CSV header.")
                    isin_col_index = -1 # Indicate failure

            if isin_col_index != -1:
                 with open(NIFTY_100_CSV, 'r', encoding='utf-8') as f_data:
                     next(f_data, None) # Skip header row
                     reader_data = csv.reader(f_data)
                     for row in reader_data:
                         if len(row) > isin_col_index:
                             isin_val = row[isin_col_index]
                             if isin_val:
                                 isins.add(isin_val.strip())
            print(f"    Loaded {len(isins)} Nifty 100 ISINs.")
        except Exception as e:
            print(f"    Error loading Nifty 100 CSV: {e}")
            # Don't necessarily fail, proceed without Nifty filtering

    print("--- Stage 1 Complete: Data Acquisition Attempted ---")
    return instruments, isins


def download_file(url, dest_path, description, headers, retries=3, delay=5):
    """Download a file with retries"""
    print(f"    Downloading {description} from {url}...")
    for attempt in range(retries):
        try:
            response = requests.get(url, stream=True, headers=headers, timeout=60)
            response.raise_for_status()
            with open(dest_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"    Successfully downloaded {description} to {dest_path}.")
            return True
        except requests.exceptions.RequestException as e:
            print(f"    Error downloading {description} (Attempt {attempt + 1}/{retries}): {e}")
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                print(f"    Failed to download {description} after {retries} attempts.")
                return False
    return False

def extract_gzip(gz_path, out_path):
    """Extract a gzipped file"""
    print(f"    Extracting {os.path.basename(gz_path)}...")
    try:
        with gzip.open(gz_path, 'rb') as f_in, open(out_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
        print(f"    Successfully extracted to {os.path.basename(out_path)}.")
        return True
    except Exception as e:
        print(f"    Error extracting {gz_path}: {e}")
        return False

# --- Helper Functions: Data Processing ---

def filter_and_group_instruments(raw_instrument_list, nifty_isin_set):
    """Filters Nifty 100 stocks, groups all options by underlying, and collects keys for LTP fetch."""
    print("\n--- Stage 2: Filtering Instruments & Grouping Options ---")
    selected_stocks = []
    options_by_underlying = defaultdict(list) # Groups options by underlying_key
    all_keys_for_ltp = set() # Collect all keys (stock instrument_key, option underlying_key) needing LTP

    if not isinstance(raw_instrument_list, list):
        print("  Error: Raw instrument data is not a list.")
        return [], defaultdict(list), set()

    required_option_keys = {"instrument_key", "underlying_key", "instrument_type", "expiry"} # Ensure expiry exists
    required_equity_keys = {"instrument_key", "isin", "instrument_type"}

    nifty_filter_active = bool(nifty_isin_set)
    if not nifty_filter_active:
        print("  Warning: Nifty 100 ISIN set is empty. Stocks will not be filtered by Nifty 100 inclusion.")

    processed_count = 0
    skipped_options = 0
    for inst in raw_instrument_list:
        processed_count +=1
        inst_type = inst.get("instrument_type", "")
        instrument_key = inst.get("instrument_key")

        if not instrument_key:
            continue # Skip if no instrument key

        # Process Equities
        if inst_type == "EQ" and required_equity_keys.issubset(inst.keys()):
            is_nifty_100 = nifty_filter_active and inst.get("isin") in nifty_isin_set
            if not nifty_filter_active or is_nifty_100: # Select if Nifty or if filter is inactive
                if not inst.get("short_name"):
                     inst["short_name"] = inst.get("trading_symbol", "").replace("-EQ", "").strip()
                selected_stocks.append(inst)
                all_keys_for_ltp.add(instrument_key) # Stock instrument key needs LTP

        # Process Options
        elif inst_type in ["CE", "PE"]:
             # Ensure all required keys, including 'expiry', are present
             if required_option_keys.issubset(inst.keys()):
                 underlying_key = inst.get("underlying_key")
                 if underlying_key:
                     options_by_underlying[underlying_key].append(inst)
                     all_keys_for_ltp.add(underlying_key) # Option underlying key needs LTP
             else:
                 skipped_options += 1 # Count options skipped due to missing keys

        # Progress update
        if processed_count > 0 and processed_count % 100000 == 0:
             print(f"  Processed {processed_count // 1000}k instruments...")

    print(f"  Selected {len(selected_stocks)} stocks ({'Nifty 100 filtered' if nifty_filter_active else 'All Equities'}).")
    print(f"  Grouped options under {len(options_by_underlying)} unique underlying keys.")
    if skipped_options > 0:
        print(f"  Skipped {skipped_options} options due to missing required keys (e.g., expiry).")
    print(f"  Collected {len(all_keys_for_ltp)} unique keys requiring LTP fetch.")
    print("--- Stage 2 Complete: Initial Filtering and Grouping ---")

    return selected_stocks, options_by_underlying, all_keys_for_ltp


def fetch_ltps(keys_to_fetch, access_token):
    """Fetches LTPs in batches using the correct response parsing."""
    print("\n--- Stage 3: Fetching LTPs ---")
    if not keys_to_fetch:
        print("  No keys provided for LTP fetching.")
        return {}
    if not access_token:
        print("  Access token not provided. Cannot fetch LTPs.")
        return {} # Fetch cannot proceed

    print(f"  Fetching LTPs for {len(keys_to_fetch)} keys...")
    ltp_map = {}
    keys_list = list(keys_to_fetch)
    num_batches = (len(keys_list) + LTP_BATCH_SIZE - 1) // LTP_BATCH_SIZE
    headers = {'Accept': 'application/json', 'Authorization': f'Bearer {access_token}'}

    for i in range(0, len(keys_list), LTP_BATCH_SIZE):
        batch_keys = keys_list[i : i + LTP_BATCH_SIZE]
        batch_num = (i // LTP_BATCH_SIZE) + 1
        print(f"    Fetching batch {batch_num}/{num_batches} ({len(batch_keys)} keys)...")

        instruments_param = ','.join([key.replace('|', '%7C') for key in batch_keys])
        url = f"{LTP_API_URL}?instrument_key={instruments_param}"

        try:
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            response_data = response.json()

            if response_data.get("status") == "success" and "data" in response_data:
                fetched_data = response_data["data"]
                processed_in_batch = 0
                for api_response_key, item_data in fetched_data.items():
                    if isinstance(item_data, dict):
                        instrument_token = item_data.get("instrument_token")
                        last_price = item_data.get("last_price")

                        if instrument_token and instrument_token in keys_to_fetch:
                            if isinstance(last_price, (int, float)) and not math.isnan(last_price):
                                ltp_map[instrument_token] = float(last_price)
                            else:
                                ltp_map[instrument_token] = DEFAULT_LTP_VALUE
                            processed_in_batch += 1
                    # else: Optional log for unexpected format
                print(f"      Processed {processed_in_batch} successful LTPs from batch response.")
            elif response_data.get("status") != "success":
                print(f"      API Error in batch {batch_num}: {response_data.get('errors')}")
            # else: Optional log if success but no 'data'

        except requests.exceptions.Timeout:
            print(f"      Error: Timeout fetching batch {batch_num}.")
        except requests.exceptions.HTTPError as http_err:
            print(f"      Error: HTTP Error fetching batch {batch_num}: {http_err} - {response.text}")
        except requests.exceptions.RequestException as req_err:
            print(f"      Error: Request failed for batch {batch_num}: {req_err}")
        except json.JSONDecodeError as json_err:
             print(f"      Error: Failed to decode JSON response for batch {batch_num}: {json_err}")
        except Exception as e:
            print(f"      An unexpected error occurred processing batch {batch_num}: {e}")

    # Ensure all originally requested keys have an entry in the map
    fetched_count = 0
    missing_count = 0
    for key in keys_to_fetch:
        if key not in ltp_map:
            ltp_map[key] = DEFAULT_LTP_VALUE
            missing_count += 1
        else:
            fetched_count += 1

    print(f"  Finished LTP fetch. Found {fetched_count} LTPs, assigned default value for {missing_count} keys.")
    print("--- Stage 3 Complete: LTP Fetch Attempted ---")
    return ltp_map

def _format_expiry(expiry_ts):
    """Helper function to convert expiry timestamp to YYYY-MM-DD"""
    if expiry_ts is None:
        return DEFAULT_FORMATTED_DATE
    try:
        expiry_ts_num = float(expiry_ts)
        if math.isnan(expiry_ts_num):
            raise ValueError("Timestamp is NaN")

        expiry_ts_str = str(int(expiry_ts_num))
        num_digits = len(expiry_ts_str)
        seconds_timestamp = -1

        if 12 <= num_digits <= 14: # Milliseconds
            seconds_timestamp = int(expiry_ts_num // 1000)
        elif 9 <= num_digits <= 11: # Seconds
            seconds_timestamp = int(expiry_ts_num)
        else:
            # print(f"  Warning: Invalid digit count ({num_digits}) for expiry timestamp '{expiry_ts}'.") # Optional Verbose Log
            return DEFAULT_FORMATTED_DATE

        if seconds_timestamp >= 0:
            dt_object = datetime.fromtimestamp(seconds_timestamp)
            return dt_object.strftime(DATE_FORMAT)
        else:
            return DEFAULT_FORMATTED_DATE

    except (ValueError, TypeError, OSError) as e:
        # print(f"  Warning: Could not format expiry '{expiry_ts}': {e}") # Optional Verbose Log
        return DEFAULT_FORMATTED_DATE

def enrich_and_structure_data(selected_stocks, options_by_underlying, ltp_map):
    """Enriches stocks and option groups with LTP, formats expiry, applies strike filter, and builds final lists."""
    print("\n--- Stage 4: Enriching Data, Formatting Expiry & Final Structure ---")

    # Enrich Stocks
    master_stocks = []
    for stock_data in selected_stocks:
        instrument_key = stock_data.get("instrument_key")
        stock_data['ltp'] = ltp_map.get(instrument_key, DEFAULT_LTP_VALUE)
        master_stocks.append(stock_data)
    print(f"  Enriched {len(master_stocks)} stock records with LTP.")

    # Structure, Enrich, and Format Options
    master_options = []
    total_options_processed = 0
    total_options_filtered_out = 0
    formatting_errors = 0

    print("  Processing and formatting option groups...")
    group_count = 0
    for underlying_key, option_list in options_by_underlying.items():
        group_count += 1
        if not option_list: continue

        first_option = option_list[0]
        underlying_symbol = first_option.get("underlying_symbol", "N/A")
        underlying_ltp = ltp_map.get(underlying_key, DEFAULT_LTP_VALUE)

        # --- Format expiry within each option contract ---
        formatted_options = []
        for option_contract in option_list:
            if isinstance(option_contract, dict):
                original_expiry = option_contract.get('expiry')
                option_contract['expiry_formatted'] = _format_expiry(original_expiry)
                if option_contract['expiry_formatted'] == DEFAULT_FORMATTED_DATE and original_expiry is not None:
                    formatting_errors += 1
                formatted_options.append(option_contract)
            # else: Log non-dict item if necessary

        # Apply strike filtering if enabled and LTP is valid
        final_option_list = formatted_options # Start with formatted list
        original_count = len(formatted_options)
        filtered_count = original_count

        ltp_is_valid_for_filtering = (isinstance(underlying_ltp, (int, float)) and
                                      underlying_ltp != DEFAULT_LTP_VALUE and
                                      underlying_ltp > 0)

        if FILTER_OPTION_STRIKES and ltp_is_valid_for_filtering:
            strikes = sorted(list({
                o.get("strike_price") for o in formatted_options # Use formatted list
                if isinstance(o.get("strike_price"), (int, float))
            }))

            if len(strikes) > 1:
                spacings = [round(strikes[j+1] - strikes[j], 4) for j in range(len(strikes)-1)]
                non_zero_spacings = [s for s in spacings if abs(s) > 1e-9]
                if non_zero_spacings:
                    strike_spacing = max(set(non_zero_spacings), key=non_zero_spacings.count)
                    if strike_spacing > 1e-9:
                        min_strike = underlying_ltp - (STRIKE_INTERVALS * strike_spacing)
                        max_strike = underlying_ltp + (STRIKE_INTERVALS * strike_spacing)
                        final_option_list = [ # Filter the formatted list
                            o for o in formatted_options
                            if isinstance(o.get("strike_price"), (int, float)) and
                               min_strike <= o["strike_price"] <= max_strike
                        ]
                        filtered_count = len(final_option_list)

        # Add the group to the master list
        master_options.append({
            "underlying_key": underlying_key,
            "underlying_symbol": underlying_symbol,
            "ltp": underlying_ltp,
            "options": final_option_list # Use the final (formatted and potentially filtered) list
        })

        total_options_processed += original_count
        total_options_filtered_out += (original_count - filtered_count)

        # Progress update
        if group_count > 0 and group_count % 50 == 0:
             print(f"    Processed {group_count} option groups...")


    print(f"  Processed {len(master_options)} underlying option groups ({total_options_processed} total contracts).")
    if formatting_errors > 0:
        print(f"  Warning: Encountered {formatting_errors} errors while formatting expiry dates.")
    if FILTER_OPTION_STRIKES:
        print(f"  Filtered out {total_options_filtered_out} option contracts based on strike range.")
    print("--- Stage 4 Complete: Enrichment, Formatting, and Structuring ---")

    return master_stocks, master_options


# --- Standalone Execution ---
if __name__ == "__main__":
    print("Running instrument_keys.py directly for testing...")
    print("Attempting to connect to test Redis instance...")

    try:
        # Create a client instance for this test run
        TEST_REDIS_HOST = "localhost"
        TEST_REDIS_PORT = 6379
        TEST_REDIS_DB = 0 # Use a test DB if possible, or be careful with DB 0

        test_client = Client(
            host=TEST_REDIS_HOST,
            port=TEST_REDIS_PORT,
            db=TEST_REDIS_DB,
            password=None,
            decode_responses=True
        )
        test_client.ping()
        print("Test Redis connection successful.")

        # Run the process
        process_instruments(test_client)

    except Exception as e:
        print(f"Error during standalone execution: {e}")
        import traceback
        traceback.print_exc()

    finally:
        print("Standalone execution finished.")

