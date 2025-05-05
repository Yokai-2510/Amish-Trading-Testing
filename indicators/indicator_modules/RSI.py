import pandas as pd
import numpy as np
from datetime import datetime



def process_rsi_indicator(instrument_key, data_type, config, df):
    if df.empty:
        print(f"No candle data available for {instrument_key}")
        return {}
    
    # Extract parameters from config
    parameters = config.get("parameters", {})
    rsi_length = int(parameters.get("rsi_length", 14))
    smoothing_method = parameters.get("smoothing_method", "SMA")
    smoothing_period = int(parameters.get("smoothing_period", 3))
    threshold_value = float(parameters.get("threshold_value", 70))
    comparison_operator = parameters.get("comparison_operator", ">")
    
    try:
        # Calculate RSI
        delta = df['close'].diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        
        # First average
        avg_gain = gain.rolling(window=rsi_length, min_periods=1).mean()
        avg_loss = loss.rolling(window=rsi_length, min_periods=1).mean()
        
        # Avoid division by zero
        rs = pd.Series(np.where(avg_loss != 0, avg_gain / avg_loss, 100), index=avg_gain.index)
        rsi = 100 - (100 / (1 + rs))
        
        # Apply smoothing
        if smoothing_method == "SMA":
            smooth_rsi = rsi.rolling(window=smoothing_period, min_periods=1).mean()
        elif smoothing_method == "EMA":
            smooth_rsi = rsi.ewm(span=smoothing_period, adjust=False).mean()
        elif smoothing_method == "WMA":
            weights = np.arange(1, smoothing_period + 1)
            smooth_rsi = rsi.rolling(window=smoothing_period, min_periods=1).apply(
                lambda x: np.sum(x * weights[-len(x):]) / np.sum(weights[-len(x):]), raw=True
            )
        else:
            smooth_rsi = rsi
        
        # Get latest values
        latest_rsi = rsi.iloc[-1] if not rsi.empty else None
        latest_smooth_rsi = smooth_rsi.iloc[-1] if not smooth_rsi.empty else None
        
        # Check conditions
        conditions = config.get("conditions", {})
        active_condition = str(conditions.get("active_condition", 1))
        condition_results = {
            "1": False,
            "2": False
        }
        
        # Condition 1: Plot Line Crosses below Smooth MA
        if len(rsi) >= 2 and len(smooth_rsi) >= 2:
            prev_above = rsi.iloc[-2] > smooth_rsi.iloc[-2]
            curr_below = rsi.iloc[-1] <= smooth_rsi.iloc[-1]
            condition_results["1"] = prev_above and curr_below
        
        # Condition 2: RSI compared to threshold_value
        if latest_rsi is not None:
            if comparison_operator == ">":
                condition_results["2"] = latest_rsi > threshold_value
            elif comparison_operator == "<":
                condition_results["2"] = latest_rsi < threshold_value
            elif comparison_operator == "=":
                condition_results["2"] = latest_rsi == threshold_value
        
        # Active condition result
        condition_met = condition_results.get(active_condition, False)
        
        # Prepare result
        result = {
            "rsi_value": float(latest_rsi) if latest_rsi is not None else None,
            "smooth_rsi": float(latest_smooth_rsi) if latest_smooth_rsi is not None else None,
            "threshold": threshold_value,
            "comparison_operator": comparison_operator,
            "conditions": {
                "1": bool(condition_results["1"]),
                "2": bool(condition_results["2"])
            },
            "condition_met": bool(condition_met),
            "timestamp": df['timestamp'].iloc[-1].isoformat() if not df.empty else None
        }
        
        return result
        
    except Exception as e:
        print(f"Error calculating RSI for {instrument_key}: {str(e)}")
        return {
            "error": str(e),
            "timestamp": df['timestamp'].iloc[-1].isoformat() if not df.empty else None
        }
    
    
if __name__ == '__main__'  : 
    process_rsi_indicator()