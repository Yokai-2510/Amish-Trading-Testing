import pandas as pd
from datetime import datetime

def process_trend_analysis_indicator(instrument_key, data_type, config, df):
    if df.empty:
        print(f"No candle data available for {instrument_key}")
        return {}
    
    # Extract parameters from config
    parameters = config.get("parameters", {})
    uptrend_candles = int(parameters.get("uptrend_candles", 3))
    downtrend_candles = int(parameters.get("downtrend_candles", 3))
    
    try:
        # Determine candle direction (green/red)
        df['candle_color'] = df.apply(lambda row: 'green' if row['close'] >= row['open'] else 'red', axis=1)
        
        # Calculate consecutive count of same colored candles
        green_count = 0
        red_count = 0
        
        # Start from the most recent candle and count backward
        for i in range(len(df) - 1, -1, -1):
            if df['candle_color'].iloc[i] == 'green':
                green_count += 1
                red_count = 0
            else:
                red_count += 1
                green_count = 0
                
            # Break early if we have enough data
            if i < len(df) - max(uptrend_candles, downtrend_candles):
                break
        
        # Check conditions
        conditions = config.get("conditions", {})
        active_condition = str(conditions.get("active_condition", 1))
        condition_results = {
            "1": False,
            "2": False
        }
        
        # Condition 1: Uptrend (consecutive green candles)
        condition_results["1"] = green_count >= uptrend_candles
        
        # Condition 2: Downtrend (consecutive red candles)
        condition_results["2"] = red_count >= downtrend_candles
        
        # Active condition result
        condition_met = condition_results.get(active_condition, False)
        
        # Prepare result
        result = {
            "consecutive_green": float(green_count),
            "consecutive_red": float(red_count),
            "uptrend_threshold": float(uptrend_candles),
            "downtrend_threshold": float(downtrend_candles),
            "conditions": {
                "1": bool(condition_results["1"]),
                "2": bool(condition_results["2"])
            },
            "condition_met": bool(condition_met),
            "timestamp": df['timestamp'].iloc[-1].isoformat() if not df.empty else None
        }
        
        return result
        
    except Exception as e:
        print(f"Error calculating Trend Analysis for {instrument_key}: {str(e)}")
        return {
            "error": str(e),
            "timestamp": df['timestamp'].iloc[-1].isoformat() if not df.empty else None
        }
    
if __name__ == '__main__'  : 
    process_trend_analysis_indicator()