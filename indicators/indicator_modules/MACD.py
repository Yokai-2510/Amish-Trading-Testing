import pandas as pd
from datetime import datetime

def process_macd_indicator(instrument_key, data_type, config, df):
    if df.empty:
        print(f"No candle data available for {instrument_key}")
        return {}

    # Extract MACD parameters
    parameters = config.get("parameters", {})
    fast_len = int(parameters.get("fast_ema_length", 12))
    slow_len = int(parameters.get("slow_ema_length", 26))
    signal_len = int(parameters.get("signal_line_length", 9))

    try:
        # Calculate EMAs
        fast_ema = df['close'].ewm(span=fast_len, adjust=False).mean()
        slow_ema = df['close'].ewm(span=slow_len, adjust=False).mean()

        # MACD line and signal
        macd_line = fast_ema - slow_ema
        signal_line = macd_line.ewm(span=signal_len, adjust=False).mean()
        histogram = macd_line - signal_line

        # Extract latest and previous values
        latest_macd = macd_line.iloc[-1] if not macd_line.empty else 0.0
        prev_macd = macd_line.iloc[-2] if len(macd_line) >= 2 else 0.0
        latest_signal = signal_line.iloc[-1] if not signal_line.empty else 0.0
        prev_signal = signal_line.iloc[-2] if len(signal_line) >= 2 else 0.0
        hist1 = histogram.iloc[-1] if not histogram.empty else 0.0
        hist2 = histogram.iloc[-2] if len(histogram) >= 2 else 0.0

        # Define conditions
        condition_results = {
            "1": bool((prev_macd < prev_signal) and (latest_macd > latest_signal)),  # MACD cross above signal
            "2": bool(hist2 > 0 and hist1 > 0),  # Two positive histogram bars
            "3": bool(latest_macd > 0)  # MACD above zero
        }

        # Pick active condition
        conditions = config.get("conditions", {})
        active_condition = str(conditions.get("active_condition", 1))
        condition_met = bool(condition_results.get(active_condition, False))

        # Return result
        return {
            "macd_value": float(latest_macd),
            "signal_value": float(latest_signal),
            "histogram": float(hist1),
            "conditions": {
                "1": condition_results["1"],
                "2": condition_results["2"],
                "3": condition_results["3"]
            },
            "condition_met": condition_met,
            "timestamp": df['timestamp'].iloc[-1].isoformat() if not df.empty else None
        }

    except Exception as e:
        print(f"Error calculating MACD for {instrument_key}: {str(e)}")
        return {
            "error": str(e),
            "timestamp": df['timestamp'].iloc[-1].isoformat() if not df.empty else None
        }
if __name__ == '__main__'  : 
    process_macd_indicator()