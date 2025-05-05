import requests
from datetime import datetime, timedelta

def fetch_historical_data(instrument, interval="1minute", days_back=180):
    """Fetch historical candle data from Upstox API."""
    to_date = datetime.now().strftime("%Y-%m-%d")
    from_date = (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")
    url = f"https://api.upstox.com/v2/historical-candle/{instrument}/{interval}/{to_date}/{from_date}"
    headers = {'Accept': 'application/json'}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json().get("data", {}).get("candles", [])
    except requests.RequestException as e:
        print(f"Failed to fetch data for {instrument}: {e}")
        return []
    
if __name__ == "__main__":
    data = fetch_historical_data("NSE_INDEX|Nifty Bank")
