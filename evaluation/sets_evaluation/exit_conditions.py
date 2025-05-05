import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta

class ExitConditionsEvaluator:
    def __init__(self, data: pd.DataFrame, position_type: str = 'long'):
        """
        Initialize Exit Conditions Evaluator
        
        Parameters:
        data (pd.DataFrame): Price data with columns ['timestamp', 'open', 'high', 'low', 'close', 'volume']
        position_type (str): 'long' or 'short'
        """
        self.data = data
        self.position_type = position_type
        self.entry_price = None
        self.entry_time = None
        self.current_price = None
        self.current_time = None

    def evaluate_technical_exits(self, technical_indicators: dict) -> Dict[str, bool]:
        """
        Evaluate technical indicator-based exit conditions
        
        Parameters:
        technical_indicators (dict): Dictionary containing technical indicator values
        """
        exit_signals = {
            'rsi_exit': False,
            'ma_exit': False,
            'macd_exit': False
        }
        
        # RSI Crossover Evaluation
        if 'rsi' in technical_indicators:
            rsi = technical_indicators['rsi']
            rsi_prev = rsi.shift(1)
            
            if self.position_type == 'long':
                exit_signals['rsi_exit'] = (rsi_prev > 70) & (rsi < 70)
            else:
                exit_signals['rsi_exit'] = (rsi_prev < 30) & (rsi > 30)
        
        # Moving Average Crossover Evaluation
        if all(k in technical_indicators for k in ['fast_ma', 'slow_ma']):
            fast_ma = technical_indicators['fast_ma']
            slow_ma = technical_indicators['slow_ma']
            
            if self.position_type == 'long':
                exit_signals['ma_exit'] = (fast_ma < slow_ma) & (fast_ma.shift(1) > slow_ma.shift(1))
            else:
                exit_signals['ma_exit'] = (fast_ma > slow_ma) & (fast_ma.shift(1) < slow_ma.shift(1))
        
        # MACD Signal Line Crossover
        if all(k in technical_indicators for k in ['macd', 'signal']):
            macd = technical_indicators['macd']
            signal = technical_indicators['signal']
            
            if self.position_type == 'long':
                exit_signals['macd_exit'] = (macd < signal) & (macd.shift(1) > signal.shift(1))
            else:
                exit_signals['macd_exit'] = (macd > signal) & (macd.shift(1) < signal.shift(1))
        
        return exit_signals

    def evaluate_price_action_exits(self, 
                                  previous_periods: int = 5,
                                  trend_candles: int = 3) -> Dict[str, bool]:
        """
        Evaluate price action based exit conditions
        """
        exit_signals = {
            'pattern_exit': False,
            'breakout_exit': False,
            'trend_exit': False
        }
        
        # Candle Pattern Recognition
        current_candle = self.data.iloc[-1]
        prev_candle = self.data.iloc[-2]
        
        # Example patterns (can be expanded)
        if self.position_type == 'long':
            # Bearish engulfing
            exit_signals['pattern_exit'] = (
                current_candle['open'] > prev_candle['close'] and
                current_candle['close'] < prev_candle['open']
            )
        else:
            # Bullish engulfing
            exit_signals['pattern_exit'] = (
                current_candle['open'] < prev_candle['close'] and
                current_candle['close'] > prev_candle['open']
            )
        
        # Previous High/Low Breaks
        recent_high = self.data['high'].rolling(window=previous_periods).max()
        recent_low = self.data['low'].rolling(window=previous_periods).min()
        
        if self.position_type == 'long':
            exit_signals['breakout_exit'] = self.data['close'] < recent_low
        else:
            exit_signals['breakout_exit'] = self.data['close'] > recent_high
        
        # Continuous Trends
        closes = self.data['close'].tail(trend_candles)
        if self.position_type == 'long':
            exit_signals['trend_exit'] = all(closes.diff().tail(trend_candles-1) < 0)
        else:
            exit_signals['trend_exit'] = all(closes.diff().tail(trend_candles-1) > 0)
        
        return exit_signals

    def evaluate_risk_management_exits(self,
                                     stop_loss: float,
                                     take_profit: float,
                                     max_duration: int = None) -> Dict[str, bool]:
        """
        Evaluate risk management based exit conditions
        Parameters:
        stop_loss (float): Stop loss percentage
        take_profit (float): Take profit percentage
        max_duration (int): Maximum position duration in minutes
        """
        if self.entry_price is None:
            return {'sl_exit': False, 'tp_exit': False, 'time_exit': False}
        
        current_price = self.data['close'].iloc[-1]
        price_change = (current_price - self.entry_price) / self.entry_price * 100
        
        if self.position_type == 'long':
            sl_triggered = price_change < -stop_loss
            tp_triggered = price_change > take_profit
        else:
            sl_triggered = price_change > stop_loss
            tp_triggered = price_change < -take_profit
        
        # Time-based exit
        time_exit = False
        if max_duration and self.entry_time:
            current_time = pd.to_datetime(self.data.index[-1])
            elapsed_time = (current_time - self.entry_time).total_seconds() / 60
            time_exit = elapsed_time > max_duration
        
        return {
            'sl_exit': sl_triggered,
            'tp_exit': tp_triggered,
            'time_exit': time_exit
        }

    def evaluate_ltp_based_exits(self,
                                price_target: float = None,
                                percentage_target: float = None) -> Dict[str, bool]:
        """
        Evaluate Last Traded Price based exit conditions
        """
        if self.entry_price is None:
            return {'price_target_exit': False, 'percentage_target_exit': False}
        
        current_price = self.data['close'].iloc[-1]
        
        # LTP Price target
        price_target_exit = False
        if price_target:
            if self.position_type == 'long':
                price_target_exit = current_price >= price_target
            else:
                price_target_exit = current_price <= price_target
        
        # LTP Percentage target
        percentage_target_exit = False
        if percentage_target:
            price_change = (current_price - self.entry_price) / self.entry_price * 100
            if self.position_type == 'long':
                percentage_target_exit = price_change >= percentage_target
            else:
                percentage_target_exit = price_change <= -percentage_target
        
        return {
            'price_target_exit': price_target_exit,
            'percentage_target_exit': percentage_target_exit
        }

    def should_exit(self,
                   technical_indicators: dict,
                   stop_loss: float,
                   take_profit: float,
                   max_duration: int = None,
                   price_target: float = None,
                   percentage_target: float = None,
                   trend_candles: int = 3) -> Tuple[bool, str]:
        """
        Comprehensive exit evaluation combining all conditions
        
        Returns:
        Tuple[bool, str]: (exit_flag, exit_reason)
        """
        # Evaluate all exit conditions
        technical_exits = self.evaluate_technical_exits(technical_indicators)
        price_action_exits = self.evaluate_price_action_exits(trend_candles=trend_candles)
        risk_exits = self.evaluate_risk_management_exits(stop_loss, take_profit, max_duration)
        ltp_exits = self.evaluate_ltp_based_exits(price_target, percentage_target)
        
        # Combine all exit signals
        exit_reasons = []
        
        if any(technical_exits.values()):
            exit_reasons.extend([k for k, v in technical_exits.items() if v])
        
        if any(price_action_exits.values()):
            exit_reasons.extend([k for k, v in price_action_exits.items() if v])
        
        if any(risk_exits.values()):
            exit_reasons.extend([k for k, v in risk_exits.items() if v])
        
        if any(ltp_exits.values()):
            exit_reasons.extend([k for k, v in ltp_exits.items() if v])
        
        should_exit = len(exit_reasons) > 0
        exit_reason = ' & '.join(exit_reasons) if should_exit else ''
        
        return should_exit, exit_reason

def main():
    # Example usage
    data = pd.read_csv('price_data.csv')
    data['timestamp'] = pd.to_datetime(data['timestamp'])
    data.set_index('timestamp', inplace=True)
    
    # Initialize evaluator
    evaluator = ExitConditionsEvaluator(data, position_type='long')
    
    # Set entry parameters
    evaluator.entry_price = data['close'].iloc[0]
    evaluator.entry_time = data.index[0]
    
    # Example technical indicators
    technical_indicators = {
        'rsi': pd.Series(np.random.rand(len(data)) * 100),  # Example RSI values
        'fast_ma': data['close'].rolling(window=10).mean(),
        'slow_ma': data['close'].rolling(window=20).mean(),
        'macd': pd.Series(np.random.rand(len(data))),
        'signal': pd.Series(np.random.rand(len(data)))
    }
    
    # Evaluate exit conditions
    should_exit, exit_reason = evaluator.should_exit(
        technical_indicators=technical_indicators,
        stop_loss=2.0,
        take_profit=5.0,
        max_duration=120,
        price_target=105.0,
        percentage_target=3.0,
        trend_candles=3
    )
    
    print(f"Should Exit: {should_exit}")
    print(f"Exit Reason: {exit_reason}")

if __name__ == "__main__":
    main()