from rejson import Client, Path
import pandas as pd

from indicators.indicator_modules.RSI import process_rsi_indicator
from indicators.indicator_modules.MA import process_ma_indicator
from indicators.indicator_modules.Stoch_RSI import process_stoch_rsi_indicator
from indicators.indicator_modules.MACD import process_macd_indicator
from indicators.indicator_modules.Bollinger_Bands import process_bb_indicator
from indicators.indicator_modules.Trend_Analysis import process_trend_analysis_indicator
from indicators.indicator_modules.ADX import process_adx_indicator
from indicators.indicator_modules.Supertrend import process_supertrend_indicator
from indicators.indicator_modules.Fibonacci import process_fibonacci_indicator


def get_redis_client():
    REDIS_HOST = "localhost"
    REDIS_PORT = 6379
    REDIS_DB = 0
    REDIS_PASSWORD = None
    return Client(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PASSWORD, decode_responses=True)

def convert_to_heikin_ashi(df):
    ha_df = df.copy()
    ha_df['close'] = (df['open'] + df['high'] + df['low'] + df['close']) / 4
    ha_df['open'] = ((df['open'].shift(1) + df['close'].shift(1)) / 2).fillna(df['open'])
    ha_df['high'] = df[['high', 'open', 'close']].max(axis=1)
    ha_df['low'] = df[['low', 'open', 'close']].min(axis=1)
    return ha_df

def convert_to_renko(df, brick_size=10):
    renko_data = []
    last_price = df['close'].iloc[0] if not df.empty else 0
    for _, row in df.iterrows():
        price = row['close']
        bricks = int((price - last_price) / brick_size)
        if abs(bricks) >= 1:
            for i in range(abs(bricks)):
                brick_price = last_price + (brick_size * (1 if bricks > 0 else -1) * (i + 1))
                renko_data.append({
                    'timestamp': row['timestamp'],
                    'open': brick_price - brick_size if bricks > 0 else brick_price,
                    'high': brick_price if bricks > 0 else brick_price + brick_size,
                    'low': brick_price - brick_size if bricks > 0 else brick_price,
                    'close': brick_price,
                    'volume': row['volume'] // abs(bricks) if bricks != 0 else row['volume']
                })
            last_price = brick_price
    return pd.DataFrame(renko_data) if renko_data else pd.DataFrame()

def resample_dataframe(df, timeframe):
    timeframe_map = {
        '1m': '1min', '3m': '3min', '5m': '5min', '15m': '15min', '30m': '30min',
        '1h': '1H', '1d': '1D', '1W': '1W'
    }
    if timeframe not in timeframe_map:
        print(f"Invalid timeframe {timeframe}, using original data")
        return df
    
    if df.empty:
        return df
    
    df = df.set_index('timestamp')
    rule = timeframe_map[timeframe]
    resampled = df.resample(rule).agg({
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
        'volume': 'sum'
    }).dropna()
    return resampled.reset_index()

def get_candle_dataframe(instrument_key, data_type="stocks", chart_type="candlestick", timeframe="15m"):
    r = get_redis_client()
    complete_path = f".data_streams.candle_data.complete_candles.{data_type}"
    complete_data = r.jsonget("trading_setup", Path(complete_path)) or {}
    candles = complete_data.get(instrument_key, [])
    
    if not candles:
        print(f"No candle data for {instrument_key}")
        return pd.DataFrame()
    
    normalized = [
        {
            "timestamp": c["timestamp"],
            "open": float(c["open"]),
            "high": float(c["high"]),
            "low": float(c["low"]),
            "close": float(c["close"]),
            "volume": int(c["volume"])
        }
        for c in candles
    ]
    df = pd.DataFrame(normalized)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df.sort_values("timestamp", inplace=True)
    
    df = resample_dataframe(df, timeframe)
    
    if chart_type.lower() == "heikin ashi":
        df = convert_to_heikin_ashi(df)
    elif chart_type.lower() == "renko":
        df = convert_to_renko(df)
    
    return df

def get_instrument_key(r, identifier, data_type="stocks"):
    if data_type == "stocks":
        stocks = r.jsonget("trading_setup", Path(".instruments.instrument_stocks")) or []
        for stock in stocks:
            if stock.get("short_name") == identifier:
                return stock.get("instrument_key")
    elif data_type == "options":
        options = r.jsonget("trading_setup", Path(".instruments.instrument_options")) or []
        for opt in options:
            if opt.get("underlying_symbol") == identifier:
                return opt.get("underlying_key")
    return None

def process_indicator(instrument_key, data_type, indicator_name, indicator_config, df):
    ind_type = indicator_config.get("type")
    
    if ind_type == "RSI":
        return process_rsi_indicator(instrument_key, data_type, indicator_config, df)
    
    elif ind_type == "MA":
        return process_ma_indicator(instrument_key, data_type, indicator_config, df)
    
    elif ind_type == "MACD":
        return process_macd_indicator(instrument_key, data_type, indicator_config, df)
    
    elif ind_type == "Stochastic RSI":
        return process_stoch_rsi_indicator(instrument_key, data_type, indicator_config, df)
    
    elif ind_type == "Bollinger Bands":
        return process_bb_indicator(instrument_key, data_type, indicator_config, df)
    
    elif ind_type == "ADX":
        return process_adx_indicator(instrument_key, data_type, indicator_config, df)
    
    elif ind_type == "Supertrend":
        return process_supertrend_indicator(instrument_key, data_type, indicator_config, df)
    
    # elif ind_type == "Volume Analysis":
    #     from indicator_modules.Volume_Analysis import process_volume_indicator
    #     return process_volume_indicator(instrument_key, data_type, indicator_config, df)
    
    elif ind_type == "Fibonacci Trend":
        return process_fibonacci_indicator(instrument_key, data_type, indicator_config, df)
    
    elif ind_type == "Trend Analysis":
        return process_trend_analysis_indicator(instrument_key, data_type, indicator_config, df)
    
    return None


def process_instruments_indicators(r, instruments, data_type, strategy_config):
    indicators_result = {}
    
    for instrument in instruments:
        identifier = instrument.get("short_name" if data_type == "stocks" else "underlying_symbol")
        instrument_key = get_instrument_key(r, identifier, data_type)
        
        if not instrument_key:
            print(f"No instrument key found for {identifier}")
            continue
        
        # Get chart type and timeframe
        chart_type = strategy_config.get("basic_config", {}).get("exit_config", {}).get("chart_type", "candlestick")
        timeframe = strategy_config.get("basic_config", {}).get("exit_config", {}).get("time_frame", "15m")
        indicators_config = strategy_config.get("exit_indicators", {})
        
        df = get_candle_dataframe(instrument_key, data_type, chart_type, timeframe)
        if df.empty:
            print(f"No candle data for {instrument_key}")
            continue
        
        indicators_result[instrument_key] = {}
        for ind_name, config in indicators_config.items():
            result = process_indicator(instrument_key, data_type, ind_name, config, df)
            if result:
                indicators_result[instrument_key][ind_name] = result
    
    return indicators_result


def update_exit_indicators():
    r = get_redis_client()
    
    strategy_stocks = r.jsonget("trading_setup", Path(".configurations.strategy.stocks")) or {}
    strategy_options = r.jsonget("trading_setup", Path(".configurations.strategy.options")) or {}
    active_stocks = r.jsonget("trading_setup", Path(".instruments.active_stocks")) or []
    active_options = r.jsonget("trading_setup", Path(".instruments.active_options")) or []
    
    stocks_indicators = process_instruments_indicators(r, active_stocks, "stocks", strategy_stocks)
    options_indicators = process_instruments_indicators(r, active_options, "options", strategy_options)
    
    r.jsonset("trading_setup", Path(".indicators.stocks.exit_indicators"), stocks_indicators)
    r.jsonset("trading_setup", Path(".indicators.options.exit_indicators"), options_indicators)
    


if __name__ == "__main__":
    update_exit_indicators()