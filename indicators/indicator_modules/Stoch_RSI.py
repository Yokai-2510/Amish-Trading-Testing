import pandas as pd
import numpy as np
from datetime import datetime

def process_stoch_rsi_indicator(instrument_key, data_type, config, df):
    if df.empty:
        print(f"No candle data available for {instrument_key}")
        return {}
    
    # Extract parameters from config
    parameters = config.get("parameters", {})
    rsi_length = int(parameters.get("rsi_length", 14))
    stoch_length = int(parameters.get("stoch_length", 14))
    k_smoothing = int(parameters.get("k_smoothing", 3))
    d_smoothing = int(parameters.get("d_smoothing", 3))
    k_threshold = float(parameters.get("k_threshold", 80))
    
    try:
        # Check data sufficiency
        if len(df) < rsi_length + stoch_length + max(k_smoothing, d_smoothing):
            return {
                "error": f"Not enough data points. Need at least {rsi_length + stoch_length + max(k_smoothing, d_smoothing)} candles, but got {len(df)}",
                "timestamp": df['timestamp'].iloc[-1].isoformat() if not df.empty else None
            }
        
        # Calculate RSI
        delta = df['close'].diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        
        avg_gain = gain.rolling(window=rsi_length, min_periods=1).mean()
        avg_loss = loss.rolling(window=rsi_length, min_periods=1).mean()
        
        rs = pd.Series(np.where(avg_loss != 0, avg_gain / avg_loss, 100), index=avg_gain.index)
        rsi = 100 - (100 / (1 + rs))
        
        valid_rsi = rsi.dropna()
        if len(valid_rsi) < stoch_length:
            return {
                "error": "Not enough valid RSI data points for Stochastic RSI calculation",
                "timestamp": df['timestamp'].iloc[-1].isoformat() if not df.empty else None
            }
        
        # Calculate Stochastic RSI
        stoch_rsi_values = []
        for i in range(stoch_length, len(valid_rsi) + 1):
            window = valid_rsi.iloc[i-stoch_length:i]
            min_rsi = window.min()
            max_rsi = window.max()
            current_rsi = valid_rsi.iloc[i-1]
            if max_rsi == min_rsi:
                stoch_rsi_values.append(50.0)
            else:
                stoch_val = ((current_rsi - min_rsi) / (max_rsi - min_rsi)) * 100
                stoch_rsi_values.append(stoch_val)
        
        date_index = valid_rsi.index[stoch_length-1:]
        stoch_rsi_k = pd.Series(stoch_rsi_values, index=date_index)
        
        # Smooth K and D lines
        k_line = stoch_rsi_k.rolling(window=k_smoothing, min_periods=1).mean()
        d_line = k_line.rolling(window=d_smoothing, min_periods=1).mean()
        
        # Get latest values
        latest_stoch_rsi = stoch_rsi_k.iloc[-1] if not stoch_rsi_k.empty else 0.0
        latest_k = k_line.iloc[-1] if not k_line.empty and not pd.isna(k_line.iloc[-1]) else 0.0
        latest_d = d_line.iloc[-1] if not d_line.empty and not pd.isna(d_line.iloc[-1]) else 0.0
        
        # Check conditions
        conditions = config.get("conditions", {})
        active_condition = str(conditions.get("active_condition", 1))
        condition_results = {
            "1": False,
            "2": False
        }
        
        # Condition 1: %K crosses above %D
        if len(k_line) >= 2 and len(d_line) >= 2:
            prev_k = k_line.iloc[-2]
            prev_d = d_line.iloc[-2]
            curr_k = k_line.iloc[-1]
            curr_d = d_line.iloc[-1]
            if not pd.isna(prev_k) and not pd.isna(prev_d) and not pd.isna(curr_k) and not pd.isna(curr_d):
                prev_k_below = prev_k <= prev_d
                curr_k_above = curr_k > curr_d
                condition_results["1"] = prev_k_below and curr_k_above
        
        # Condition 2: %K greater than threshold
        condition_results["2"] = latest_k > k_threshold
        
        # Active condition result
        condition_met = condition_results.get(active_condition, False)
        
        # Prepare result
        result = {
            "stoch_rsi_value": float(latest_stoch_rsi),
            "k_value": float(latest_k),
            "d_value": float(latest_d),
            "k_threshold": k_threshold,
            "rsi_value": float(valid_rsi.iloc[-1]),
            "conditions": {
                "1": bool(condition_results["1"]),
                "2": bool(condition_results["2"])
            },
            "condition_met": bool(condition_met),
            "timestamp": df['timestamp'].iloc[-1].isoformat() if not df.empty else None
        }
        
        return result
    
    except Exception as e:
        print(f"Error calculating Stochastic RSI for {instrument_key}: {str(e)}")
        return {
            "error": str(e),
            "timestamp": df['timestamp'].iloc[-1].isoformat() if not df.empty else None
        }
    
if __name__ == '__main__':
    process_stoch_rsi_indicator()