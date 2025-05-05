import pandas as pd
from datetime import datetime

def process_adx_indicator(instrument_key, data_type, config, df):
    if df.empty:
        print(f"No candle data available for {instrument_key}")
        return {}
    
    # Extract parameters
    parameters = config.get("parameters", {})
    adx_smoothing_period = int(parameters.get("adx_smoothing_period", 14))
    di_length = int(parameters.get("di_length", 14))
    upward_strength_threshold = float(parameters.get("upward_strength_threshold", 25))
    
    try:
        # Calculate True Range (TR)
        df['high_low'] = df['high'] - df['low']
        df['high_prev_close'] = abs(df['high'] - df['close'].shift(1))
        df['low_prev_close'] = abs(df['low'] - df['close'].shift(1))
        df['tr'] = df[['high_low', 'high_prev_close', 'low_prev_close']].max(axis=1)
        
        # Calculate Directional Movement (+DM, -DM)
        df['plus_dm'] = df['high'].diff()
        df['minus_dm'] = -df['low'].diff()
        df['plus_dm'] = df['plus_dm'].where((df['plus_dm'] > df['minus_dm']) & (df['plus_dm'] > 0), 0)
        df['minus_dm'] = df['minus_dm'].where((df['minus_dm'] > df['plus_dm']) & (df['minus_dm'] > 0), 0)
        
        # Smooth TR, +DM, -DM using Wilder's method
        tr_smoothed = df['tr'].rolling(window=di_length, min_periods=1).mean()
        plus_dm_smoothed = df['plus_dm'].rolling(window=di_length, min_periods=1).mean()
        minus_dm_smoothed = df['minus_dm'].rolling(window=di_length, min_periods=1).mean()
        
        # Calculate +DI and -DI
        df['plus_di'] = 100 * (plus_dm_smoothed / tr_smoothed)
        df['minus_di'] = 100 * (minus_dm_smoothed / tr_smoothed)
        
        # Calculate DX and ADX
        df['dx'] = 100 * abs(df['plus_di'] - df['minus_di']) / (df['plus_di'] + df['minus_di'])
        df['adx'] = df['dx'].rolling(window=adx_smoothing_period, min_periods=1).mean()
        
        # Get latest values
        latest_adx = df['adx'].iloc[-1] if not df['adx'].empty else 0.0
        latest_plus_di = df['plus_di'].iloc[-1] if not df['plus_di'].empty else 0.0
        latest_minus_di = df['minus_di'].iloc[-1] if not df['minus_di'].empty else 0.0
        
        # Check conditions
        conditions = config.get("conditions", {})
        active_condition = str(conditions.get("active_condition", 1))
        condition_results = {
            "1": False,
            "2": False
        }
        
        # Condition 1: ADX above threshold
        condition_results["1"] = latest_adx > upward_strength_threshold if not pd.isna(latest_adx) else False
        
        # Condition 2: ADX below threshold
        condition_results["2"] = latest_adx < upward_strength_threshold if not pd.isna(latest_adx) else False
        
        # Active condition result
        condition_met = condition_results.get(active_condition, False)
        
        # Prepare result
        result = {
            "adx_value": float(latest_adx),
            "plus_di": float(latest_plus_di),
            "minus_di": float(latest_minus_di),
            "upward_strength_threshold": float(upward_strength_threshold),
            "conditions": {
                "1": bool(condition_results["1"]),
                "2": bool(condition_results["2"])
            },
            "condition_met": bool(condition_met),
            "timestamp": df['timestamp'].iloc[-1].isoformat() if not df.empty else None
        }
        
        return result
        
    except Exception as e:
        print(f"Error calculating ADX for {instrument_key}: {str(e)}")
        return {
            "error": str(e),
            "timestamp": df['timestamp'].iloc[-1].isoformat() if not df.empty else None
        }