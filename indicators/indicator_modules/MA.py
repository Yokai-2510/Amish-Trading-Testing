import pandas as pd
import numpy as np
from datetime import datetime

def process_ma_indicator(instrument_key, data_type, config, df):
    if df.empty:
        print(f"No candle data available for {instrument_key}")
        return {}
    
    # Extract parameters from config
    parameters = config.get("parameters", {})
    ma_length = int(parameters.get("ma_length", 20))
    source_data = parameters.get("source_data", "Close").lower()
    offset = int(parameters.get("offset", 0))
    smoothing_method = parameters.get("smoothing_method", "SMA").upper()
    
    # Validate source data
    valid_sources = ["open", "high", "low", "close", "hl2", "hlc3", "ohlc4"]
    if source_data not in valid_sources:
        source_data = "close"
    
    try:
        # Prepare source data
        if source_data == "close":
            price_series = df['close']
        elif source_data == "open":
            price_series = df['open']
        elif source_data == "high":
            price_series = df['high']
        elif source_data == "low":
            price_series = df['low']
        elif source_data == "hl2":
            price_series = (df['high'] + df['low']) / 2
        elif source_data == "hlc3":
            price_series = (df['high'] + df['low'] + df['close']) / 3
        elif source_data == "ohlc4":
            price_series = (df['open'] + df['high'] + df['low'] + df['close']) / 4
        
        # Calculate MA based on smoothing method
        if smoothing_method == "SMA":
            ma_series = price_series.rolling(window=ma_length, min_periods=1).mean()
        elif smoothing_method == "EMA":
            ma_series = price_series.ewm(span=ma_length, adjust=False).mean()
        elif smoothing_method == "WMA":
            weights = np.arange(1, ma_length + 1)
            ma_series = price_series.rolling(window=ma_length, min_periods=1).apply(
                lambda x: np.sum(weights[-len(x):] * x) / np.sum(weights[-len(x):]), raw=True
            )
        else:
            ma_series = price_series.rolling(window=ma_length, min_periods=1).mean()
        
        # Apply offset
        if offset != 0:
            ma_series = ma_series.shift(offset)
        
        # Calculate smoothed MA
        smoothed_ma_length = ma_length * 2
        if smoothing_method == "SMA":
            smoothed_ma_series = price_series.rolling(window=smoothed_ma_length, min_periods=1).mean()
        elif smoothing_method == "EMA":
            smoothed_ma_series = price_series.ewm(span=smoothed_ma_length, adjust=False).mean()
        elif smoothing_method == "WMA":
            weights = np.arange(1, smoothed_ma_length + 1)
            smoothed_ma_series = price_series.rolling(window=smoothed_ma_length, min_periods=1).apply(
                lambda x: np.sum(weights[-len(x):] * x) / np.sum(weights[-len(x):]), raw=True
            )
        else:
            smoothed_ma_series = price_series.rolling(window=smoothed_ma_length, min_periods=1).mean()
        
        # Get recent values
        ma_current = ma_series.iloc[-1] if not ma_series.empty else None
        ma_prev = ma_series.iloc[-2] if len(ma_series) >= 2 else None
        smoothed_ma_current = smoothed_ma_series.iloc[-1] if not smoothed_ma_series.empty else None
        smoothed_ma_prev = smoothed_ma_series.iloc[-2] if len(smoothed_ma_series) >= 2 else None
        
        close_current = df['close'].iloc[-1] if not df.empty else None
        close_prev = df['close'].iloc[-2] if len(df) >= 2 else None
        
        # Check conditions
        conditions = config.get("conditions", {})
        active_condition = str(conditions.get("active_condition", 1))
        condition_results = {
            "1": False,
            "2": False,
            "3": False,
            "4": False
        }
        
        # Condition 1: Price crosses above MA
        if close_prev is not None and ma_prev is not None and close_current is not None and ma_current is not None:
            condition_results["1"] = close_prev <= ma_prev and close_current > ma_current
        
        # Condition 2: Price closes above MA
        if close_current is not None and ma_current is not None:
            condition_results["2"] = close_current > ma_current
        
        # Condition 3: Two consecutive closes above MA
        if close_prev is not None and close_current is not None and ma_prev is not None and ma_current is not None:
            condition_results["3"] = close_prev > ma_prev and close_current > ma_current
        
        # Condition 4: MA crosses above smoothed MA
        if ma_prev is not None and smoothed_ma_prev is not None and ma_current is not None and smoothed_ma_current is not None:
            condition_results["4"] = ma_prev <= smoothed_ma_prev and ma_current > smoothed_ma_current
        
        # Active condition result
        condition_met = condition_results.get(active_condition, False)
        
        # Prepare result
        result = {
            "ma_value": float(ma_current) if ma_current is not None else None,
            "smoothed_ma": float(smoothed_ma_current) if smoothed_ma_current is not None else None,
            "current_price": float(close_current) if close_current is not None else None,
            "conditions": {
                "1": bool(condition_results["1"]),
                "2": bool(condition_results["2"]),
                "3": bool(condition_results["3"]),
                "4": bool(condition_results["4"])
            },
            "condition_met": bool(condition_met),
            "timestamp": df['timestamp'].iloc[-1].isoformat() if not df.empty else None
        }
        
        return result
        
    except Exception as e:
        print(f"Error calculating MA for {instrument_key}: {str(e)}")
        return {
            "error": str(e),
            "timestamp": df['timestamp'].iloc[-1].isoformat() if not df.empty else None
        }
    
if __name__ == '__main__'  : 
    process_ma_indicator()