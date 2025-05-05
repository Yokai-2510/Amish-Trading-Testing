# File: brokers_api/upstox/candle_data/intraday_data_api.py
import requests
import time

def fetch_intraday_data(instrument):
    """Fetch intraday candle data from Upstox API."""
    url = f"https://api.upstox.com/v2/historical-candle/intraday/{instrument}/1minute"
    headers = {'Accept': 'application/json'}
    
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        if data.get("status") == "success":
            return data.get("data", {}).get("candles", [])
        else:
            print(f"API error for {instrument}: {data.get('message', 'Unknown error')}")
            return []
    except requests.RequestException as e:
        print(f"Failed to fetch intraday data for {instrument}: {e}")
        return []

# Example usage (for testing)
if __name__ == "__main__":
    instrument = "NSE_INDEX|Nifty Bank"
    candles = fetch_intraday_data(instrument)
    print(candles)