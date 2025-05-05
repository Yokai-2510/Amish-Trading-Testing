import pandas as pd
from datetime import datetime

def process_fibonacci_indicator(instrument_key, data_type, config, df):
    if df.empty:
        print(f"No candle data available for {instrument_key}")
        return {}
    
    # Extract parameters
    parameters = config.get("parameters", {})
    lookback_period = int(parameters.get("lookback_period", 20))
    fibonacci_level = float(parameters.get("fibonacci_level", 0.5))
    reaction_tolerance = float(parameters.get("reaction_tolerance", 0.01))
    
    try:
        # Standard Fibonacci levels
        fib_levels = [0.236, 0.382, 0.5, 0.618, 0.786, 1.0, 1.618, 2.618]
        
        # Get recent data within lookback period
        recent_df = df.tail(lookback_period)
        
        # Find swing high and low
        swing_high = recent_df['high'].max()
        swing_low = recent_df['low'].min()
        price_range = swing_high - swing_low
        
        # Calculate Fibonacci levels
        fib_prices = {level: swing_low + (level * price_range) for level in fib_levels}
        selected_fib_price = fib_prices.get(fibonacci_level, swing_low + (0.5 * price_range))
        
        # Get latest price
        latest_close = df['close'].iloc[-1] if not df.empty else 0.0
        
        # Check conditions
        conditions = config.get("conditions", {})
        active_condition = str(conditions.get("active_condition", 1))
        condition_results = {
            "1": False,
            "2": False
        }
        
        # Condition 1: Price near Fibonacci level (within tolerance)
        tolerance = selected_fib_price * reaction_tolerance
        condition_results["1"] = (selected_fib_price - tolerance <= latest_close <= selected_fib_price + tolerance) if not pd.isna(latest_close) else False
        
        # Condition 2: Price crosses above Fibonacci level
        prev_close = df['close'].iloc[-2] if len(df) >= 2 else latest_close
        condition_results["2"] = (prev_close <= selected_fib_price and latest_close > selected_fib_price) if not pd.isna(latest_close) and not pd.isna(prev_close) else False
        
        # Active condition result
        condition_met = condition_results.get(active_condition, False)
        
        # Prepare result
        result = {
            "fib_levels": {str(level): float(price) for level, price in fib_prices.items()},
            "selected_fib_level": float(fibonacci_level),
            "selected_fib_price": float(selected_fib_price),
            "current_price": float(latest_close),
            "conditions": {
                "1": bool(condition_results["1"]),
                "2": bool(condition_results["2"])
            },
            "condition_met": bool(condition_met),
            "timestamp": df['timestamp'].iloc[-1].isoformat() if not df.empty else None
        }
        
        return result
        
    except Exception as e:
        print(f"Error calculating Fibonacci Trend for {instrument_key}: {str(e)}")
        return {
            "error": str(e),
            "timestamp": df['timestamp'].iloc[-1].isoformat() if not df.empty else None
        }