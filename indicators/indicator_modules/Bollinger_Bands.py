import pandas as pd
import numpy as np
from datetime import datetime

def process_bb_indicator(instrument_key, data_type, config, df):
    if df.empty:
        print(f"No candle data available for {instrument_key}")
        return {}

    # Extract parameters
    parameters = config.get("parameters", {})
    ma_length = int(parameters.get("ma_length", 20))
    ma_type = parameters.get("ma_type", "SMA").upper()
    std_dev_multiplier = float(parameters.get("std_dev_multiplier", 2.0))
    upper_threshold = float(parameters.get("upper_threshold", 0.8))

    try:
        # Calculate median line (basis MA)
        if ma_type == "SMA":
            median_line = df['close'].rolling(window=ma_length, min_periods=1).mean()
        elif ma_type == "EMA":
            median_line = df['close'].ewm(span=ma_length, adjust=False).mean()
        elif ma_type == "WMA":
            weights = np.arange(1, ma_length + 1)
            median_line = df['close'].rolling(window=ma_length, min_periods=1).apply(
                lambda x: np.sum(weights[-len(x):] * x) / np.sum(weights[-len(x):]), raw=True
            )
        else:
            median_line = df['close'].rolling(window=ma_length, min_periods=1).mean()

        # Calculate standard deviation
        rolling_std = df['close'].rolling(window=ma_length, min_periods=1).std()

        # Calculate upper and lower bands
        upper_band = median_line + (std_dev_multiplier * rolling_std)
        lower_band = median_line - (std_dev_multiplier * rolling_std)

        # Get latest values
        latest_close = df['close'].iloc[-1] if not df.empty else 0.0
        latest_median = median_line.iloc[-1] if not median_line.empty else 0.0
        latest_upper = upper_band.iloc[-1] if not upper_band.empty else 0.0
        latest_lower = lower_band.iloc[-1] if not lower_band.empty else 0.0

        # Check conditions
        conditions = config.get("conditions", {})
        active_condition = str(conditions.get("active_condition", 1))
        condition_results = {
            "1": False,
            "2": False
        }

        # Condition 1: Price closes above median line
        condition_results["1"] = latest_close > latest_median if latest_close is not None and latest_median is not None else False

        # Condition 2: Price reaches upper threshold
        condition_results["2"] = latest_close > upper_threshold if latest_close is not None else False

        # Active condition result
        condition_met = condition_results.get(active_condition, False)

        # Return result
        return {
            "median_line": float(latest_median),
            "upper_band": float(latest_upper),
            "lower_band": float(latest_lower),
            "current_price": float(latest_close),
            "upper_threshold": float(upper_threshold),
            "conditions": {
                "1": bool(condition_results["1"]),
                "2": bool(condition_results["2"])
            },
            "condition_met": bool(condition_met),
            "timestamp": df['timestamp'].iloc[-1].isoformat() if not df.empty else None
        }

    except Exception as e:
        print(f"Error calculating Bollinger Bands for {instrument_key}: {str(e)}")
        return {
            "error": str(e),
            "timestamp": df['timestamp'].iloc[-1].isoformat() if not df.empty else None
        }