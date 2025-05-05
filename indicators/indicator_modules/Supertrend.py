import pandas as pd
from datetime import datetime

def process_supertrend_indicator(instrument_key, data_type, config, df):
    if df.empty:
        print(f"No candle data available for {instrument_key}")
        return {}
    
    # Extract parameters
    parameters = config.get("parameters", {})
    atr_length = int(parameters.get("atr_length", 10))
    multiplier_factor = float(parameters.get("multiplier_factor", 3.0))
    
    try:
        # Calculate True Range (TR)
        df['high_low'] = df['high'] - df['low']
        df['high_prev_close'] = abs(df['high'] - df['close'].shift(1))
        df['low_prev_close'] = abs(df['low'] - df['close'].shift(1))
        df['tr'] = df[['high_low', 'high_prev_close', 'low_prev_close']].max(axis=1)
        
        # Calculate ATR
        df['atr'] = df['tr'].rolling(window=atr_length, min_periods=1).mean()
        
        # Initialize Supertrend
        df['basic_upper_band'] = (df['high'] + df['low']) / 2 + (multiplier_factor * df['atr'])
        df['basic_lower_band'] = (df['high'] + df['low']) / 2 - (multiplier_factor * df['atr'])
        df['supertrend'] = pd.Series(index=df.index, dtype=float)
        df['trend_direction'] = pd.Series(index=df.index, dtype=str)
        
        # Initialize first values
        if len(df) > 0:
            df['supertrend'].iloc[0] = df['basic_lower_band'].iloc[0]
            df['trend_direction'].iloc[0] = 'up' if df['close'].iloc[0] > df['supertrend'].iloc[0] else 'down'
        
        # Calculate Supertrend
        for i in range(1, len(df)):
            if df['trend_direction'].iloc[i-1] == 'up':
                df['supertrend'].iloc[i] = df['basic_lower_band'].iloc[i]
                if df['close'].iloc[i] < df['supertrend'].iloc[i]:
                    df['trend_direction'].iloc[i] = 'down'
                    df['supertrend'].iloc[i] = df['basic_upper_band'].iloc[i]
                else:
                    df['trend_direction'].iloc[i] = 'up'
            else:
                df['supertrend'].iloc[i] = df['basic_upper_band'].iloc[i]
                if df['close'].iloc[i] > df['supertrend'].iloc[i]:
                    df['trend_direction'].iloc[i] = 'up'
                    df['supertrend'].iloc[i] = df['basic_lower_band'].iloc[i]
                else:
                    df['trend_direction'].iloc[i] = 'down'
        
        # Get latest values
        latest_supertrend = df['supertrend'].iloc[-1] if not df['supertrend'].empty else 0.0
        latest_trend_direction = df['trend_direction'].iloc[-1] if not df['trend_direction'].empty else 'unknown'
        latest_close = df['close'].iloc[-1] if not df.empty else 0.0
        
        # Check conditions
        conditions = config.get("conditions", {})
        active_condition = str(conditions.get("active_condition", 1))
        condition_results = {
            "1": False,
            "2": False
        }
        
        # Condition 1: Uptrend (Supertrend below price)
        condition_results["1"] = latest_trend_direction == 'up' if latest_trend_direction != 'unknown' else False
        
        # Condition 2: Downtrend (Supertrend above price)
        condition_results["2"] = latest_trend_direction == 'down' if latest_trend_direction != 'unknown' else False
        
        # Active condition result
        condition_met = condition_results.get(active_condition, False)
        
        # Prepare result
        result = {
            "supertrend_value": float(latest_supertrend),
            "trend_direction": latest_trend_direction,
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
        print(f"Error calculating Supertrend for {instrument_key}: {str(e)}")
        return {
            "error": str(e),
            "timestamp": df['timestamp'].iloc[-1].isoformat() if not df.empty else None
        }