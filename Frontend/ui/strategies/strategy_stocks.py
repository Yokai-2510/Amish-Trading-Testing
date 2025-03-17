import customtkinter as Ctk

# Import individual tab modules
from ui.strategies.tabs.stocks_config import StocksTab
from ui.strategies.tabs.sets_config import SetTab
from ui.strategies.tabs.entry_indicators_setup import EntryIndicatorsTab
from ui.strategies.tabs.exit_indicator_setup import ExitIndicatorsTab
from ui.strategies.tabs.exit_conditions import EntryExitConfigurationsTab



class StrategyStocks(Ctk.CTkFrame):
    def __init__(self, parent, set_name=None):
        super().__init__(parent)
        # Initialize the tabview
        self.tabview = Ctk.CTkTabview(self)
        self.tabview.pack(pady=20, padx=10, fill="both", expand=True)
        
        # Add all tabs
        self.tabview.add("Set")
        self.tabview.add("Stocks")
        self.tabview.add("Entry Indicators")
        self.tabview.add("Exit Indicators")
        self.tabview.add("Exit/Exit Config")
        
        # Initialize each tab with its module
        self.stocks_tab = StocksTab(self.tabview.tab("Stocks"))
        self.set_tab = SetTab(self.tabview.tab("Set"))
        self.entry_indicators_tab = EntryIndicatorsTab(self.tabview.tab("Entry Indicators"))
        self.exit_setup_tab = ExitIndicatorsTab(self.tabview.tab("Exit Indicators"))
        self.exit_conditions_tab = EntryExitConfigurationsTab(self.tabview.tab("Exit/Exit Config"))
        
        # Set the initial name if provided
        if set_name:
            self.set_tab.set_name_entry.insert(0, set_name)







"""

        # --- Indicators Tab ---
        indicators_tab = self.tabview.tab("Indicators")
        indicators_tab.grid_columnconfigure(0, weight=1)
        indicators_tab.grid_columnconfigure(1, weight=3)

        # Create scrollable frame for indicators
        indicators_scrollable = Ctk.CTkScrollableFrame(indicators_tab, width=600, height=500)
        indicators_scrollable.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
        indicators_scrollable.grid_columnconfigure(0, weight=1)
        indicators_scrollable.grid_columnconfigure(1, weight=3)

        current_row = 0

        # Bollinger Bands
        bollinger_frame = Ctk.CTkFrame(indicators_scrollable)
        bollinger_frame.grid(row=current_row, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        bollinger_frame.grid_columnconfigure(0, weight=1)
        bollinger_frame.grid_columnconfigure(1, weight=1)

        Ctk.CTkLabel(bollinger_frame, text="Bollinger Bands", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, sticky="w", padx=10, pady=(10, 5))
        Ctk.CTkLabel(bollinger_frame, text="Active:").grid(row=1, column=0, sticky="w", padx=10, pady=2)
        self.bb_active = Ctk.CTkSwitch(bollinger_frame, text="")
        self.bb_active.grid(row=1, column=1, sticky="w", padx=10, pady=2)

        Ctk.CTkLabel(bollinger_frame, text="Period:").grid(row=2, column=0, sticky="w", padx=10, pady=2)
        self.bb_period = Ctk.CTkEntry(bollinger_frame, width=80)
        self.bb_period.grid(row=2, column=1, sticky="w", padx=10, pady=2)
        self.bb_period.insert(0, "20")

        Ctk.CTkLabel(bollinger_frame, text="Standard Deviation:").grid(row=3, column=0, sticky="w", padx=10, pady=2)
        self.bb_std_dev = Ctk.CTkEntry(bollinger_frame, width=80)
        self.bb_std_dev.grid(row=3, column=1, sticky="w", padx=10, pady=2)
        self.bb_std_dev.insert(0, "2")

        Ctk.CTkLabel(bollinger_frame, text="Source:").grid(row=4, column=0, sticky="w", padx=10, pady=2)
        self.bb_source = Ctk.CTkComboBox(bollinger_frame, values=["Close", "Open", "High", "Low", "HL2", "HLC3", "OHLC4"])
        self.bb_source.grid(row=4, column=1, sticky="w", padx=10, pady=2)

        Ctk.CTkLabel(bollinger_frame, text="MBB Threshold (%):").grid(row=5, column=0, sticky="w", padx=10, pady=2)
        self.bb_threshold = Ctk.CTkEntry(bollinger_frame, width=80)
        self.bb_threshold.grid(row=5, column=1, sticky="w", padx=10, pady=2)
        self.bb_threshold.insert(0, "0.3")

        current_row += 1

        # RSI
        rsi_frame = Ctk.CTkFrame(indicators_scrollable)
        rsi_frame.grid(row=current_row, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        rsi_frame.grid_columnconfigure(0, weight=1)
        rsi_frame.grid_columnconfigure(1, weight=1)

        Ctk.CTkLabel(rsi_frame, text="RSI", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, sticky="w", padx=10, pady=(10, 5))
        Ctk.CTkLabel(rsi_frame, text="Active:").grid(row=1, column=0, sticky="w", padx=10, pady=2)
        self.rsi_active = Ctk.CTkSwitch(rsi_frame, text="")
        self.rsi_active.grid(row=1, column=1, sticky="w", padx=10, pady=2)

        Ctk.CTkLabel(rsi_frame, text="Period:").grid(row=2, column=0, sticky="w", padx=10, pady=2)
        self.rsi_period = Ctk.CTkEntry(rsi_frame, width=80)
        self.rsi_period.grid(row=2, column=1, sticky="w", padx=10, pady=2)
        self.rsi_period.insert(0, "14")

        Ctk.CTkLabel(rsi_frame, text="Overbought Level:").grid(row=3, column=0, sticky="w", padx=10, pady=2)
        self.rsi_overbought = Ctk.CTkEntry(rsi_frame, width=80)
        self.rsi_overbought.grid(row=3, column=1, sticky="w", padx=10, pady=2)
        self.rsi_overbought.insert(0, "70")

        Ctk.CTkLabel(rsi_frame, text="Oversold Level:").grid(row=4, column=0, sticky="w", padx=10, pady=2)
        self.rsi_oversold = Ctk.CTkEntry(rsi_frame, width=80)
        self.rsi_oversold.grid(row=4, column=1, sticky="w", padx=10, pady=2)
        self.rsi_oversold.insert(0, "30")

        Ctk.CTkLabel(rsi_frame, text="Source:").grid(row=5, column=0, sticky="w", padx=10, pady=2)
        self.rsi_source = Ctk.CTkComboBox(rsi_frame, values=["Close", "Open", "High", "Low", "HL2", "HLC3", "OHLC4"])
        self.rsi_source.grid(row=5, column=1, sticky="w", padx=10, pady=2)

        Ctk.CTkLabel(rsi_frame, text="Condition:").grid(row=6, column=0, sticky="w", padx=10, pady=2)
        self.rsi_condition = Ctk.CTkComboBox(rsi_frame, values=["Crossing Above Oversold", "Crossing Below Overbought", 
                                                                "Above Specific Value", "Below Specific Value", "Divergence"])
        self.rsi_condition.grid(row=6, column=1, sticky="w", padx=10, pady=2)

        Ctk.CTkLabel(rsi_frame, text="Specific Value:").grid(row=7, column=0, sticky="w", padx=10, pady=2)
        self.rsi_specific_value = Ctk.CTkEntry(rsi_frame, width=80)
        self.rsi_specific_value.grid(row=7, column=1, sticky="w", padx=10, pady=2)
        self.rsi_specific_value.insert(0, "50")

        current_row += 1

        # Stochastic RSI
        stoch_rsi_frame = Ctk.CTkFrame(indicators_scrollable)
        stoch_rsi_frame.grid(row=current_row, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        stoch_rsi_frame.grid_columnconfigure(0, weight=1)
        stoch_rsi_frame.grid_columnconfigure(1, weight=1)

        Ctk.CTkLabel(stoch_rsi_frame, text="Stochastic RSI", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, sticky="w", padx=10, pady=(10, 5))
        Ctk.CTkLabel(stoch_rsi_frame, text="Active:").grid(row=1, column=0, sticky="w", padx=10, pady=2)
        self.stoch_rsi_active = Ctk.CTkSwitch(stoch_rsi_frame, text="")
        self.stoch_rsi_active.grid(row=1, column=1, sticky="w", padx=10, pady=2)

        Ctk.CTkLabel(stoch_rsi_frame, text="K Period:").grid(row=2, column=0, sticky="w", padx=10, pady=2)
        self.stoch_rsi_k = Ctk.CTkEntry(stoch_rsi_frame, width=80)
        self.stoch_rsi_k.grid(row=2, column=1, sticky="w", padx=10, pady=2)
        self.stoch_rsi_k.insert(0, "3")

        Ctk.CTkLabel(stoch_rsi_frame, text="D Period:").grid(row=3, column=0, sticky="w", padx=10, pady=2)
        self.stoch_rsi_d = Ctk.CTkEntry(stoch_rsi_frame, width=80)
        self.stoch_rsi_d.grid(row=3, column=1, sticky="w", padx=10, pady=2)
        self.stoch_rsi_d.insert(0, "3")

        Ctk.CTkLabel(stoch_rsi_frame, text="RSI Period:").grid(row=4, column=0, sticky="w", padx=10, pady=2)
        self.stoch_rsi_period = Ctk.CTkEntry(stoch_rsi_frame, width=80)
        self.stoch_rsi_period.grid(row=4, column=1, sticky="w", padx=10, pady=2)
        self.stoch_rsi_period.insert(0, "14")

        Ctk.CTkLabel(stoch_rsi_frame, text="Stoch Period:").grid(row=5, column=0, sticky="w", padx=10, pady=2)
        self.stoch_period = Ctk.CTkEntry(stoch_rsi_frame, width=80)
        self.stoch_period.grid(row=5, column=1, sticky="w", padx=10, pady=2)
        self.stoch_period.insert(0, "14")

        Ctk.CTkLabel(stoch_rsi_frame, text="Overbought Level:").grid(row=6, column=0, sticky="w", padx=10, pady=2)
        self.stoch_rsi_overbought = Ctk.CTkEntry(stoch_rsi_frame, width=80)
        self.stoch_rsi_overbought.grid(row=6, column=1, sticky="w", padx=10, pady=2)
        self.stoch_rsi_overbought.insert(0, "80")

        Ctk.CTkLabel(stoch_rsi_frame, text="Oversold Level:").grid(row=7, column=0, sticky="w", padx=10, pady=2)
        self.stoch_rsi_oversold = Ctk.CTkEntry(stoch_rsi_frame, width=80)
        self.stoch_rsi_oversold.grid(row=7, column=1, sticky="w", padx=10, pady=2)
        self.stoch_rsi_oversold.insert(0, "20")

        Ctk.CTkLabel(stoch_rsi_frame, text="Condition:").grid(row=8, column=0, sticky="w", padx=10, pady=2)
        self.stoch_rsi_condition = Ctk.CTkComboBox(stoch_rsi_frame, values=["K Crossing Above D", "K Crossing Below D", 
                                                                            "K & D Below Oversold", "K & D Above Overbought"])
        self.stoch_rsi_condition.grid(row=8, column=1, sticky="w", padx=10, pady=2)

        current_row += 1

        # Moving Averages
        ma_frame = Ctk.CTkFrame(indicators_scrollable)
        ma_frame.grid(row=current_row, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        ma_frame.grid_columnconfigure(0, weight=1)
        ma_frame.grid_columnconfigure(1, weight=1)

        Ctk.CTkLabel(ma_frame, text="Moving Averages", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, sticky="w", padx=10, pady=(10, 5))
        Ctk.CTkLabel(ma_frame, text="Active:").grid(row=1, column=0, sticky="w", padx=10, pady=2)
        self.ma_active = Ctk.CTkSwitch(ma_frame, text="")
        self.ma_active.grid(row=1, column=1, sticky="w", padx=10, pady=2)

        Ctk.CTkLabel(ma_frame, text="MA Type:").grid(row=2, column=0, sticky="w", padx=10, pady=2)
        self.ma_type = Ctk.CTkComboBox(ma_frame, values=["Simple", "Exponential", "Weighted", "Hull"])
        self.ma_type.grid(row=2, column=1, sticky="w", padx=10, pady=2)

        Ctk.CTkLabel(ma_frame, text="Period 1:").grid(row=3, column=0, sticky="w", padx=10, pady=2)
        self.ma_period1 = Ctk.CTkEntry(ma_frame, width=80)
        self.ma_period1.grid(row=3, column=1, sticky="w", padx=10, pady=2)
        self.ma_period1.insert(0, "20")

        Ctk.CTkLabel(ma_frame, text="Period 2:").grid(row=4, column=0, sticky="w", padx=10, pady=2)
        self.ma_period2 = Ctk.CTkEntry(ma_frame, width=80)
        self.ma_period2.grid(row=4, column=1, sticky="w", padx=10, pady=2)
        self.ma_period2.insert(0, "50")

        Ctk.CTkLabel(ma_frame, text="Source:").grid(row=5, column=0, sticky="w", padx=10, pady=2)
        self.ma_source = Ctk.CTkComboBox(ma_frame, values=["Close", "Open", "High", "Low", "HL2", "HLC3", "OHLC4"])
        self.ma_source.grid(row=5, column=1, sticky="w", padx=10, pady=2)

        Ctk.CTkLabel(ma_frame, text="Condition:").grid(row=6, column=0, sticky="w", padx=10, pady=2)
        self.ma_condition = Ctk.CTkComboBox(ma_frame, values=[
            "Price Above MA", "Price Below MA", 
            "Price Crossing Above MA", "Price Crossing Below MA",
            "Fast MA Crossing Above Slow MA", "Fast MA Crossing Below Slow MA",
            "MA Slope Up", "MA Slope Down"
        ])
        self.ma_condition.grid(row=6, column=1, sticky="w", padx=10, pady=2)

        Ctk.CTkLabel(ma_frame, text="Threshold:").grid(row=7, column=0, sticky="w", padx=10, pady=2)
        self.ma_threshold = Ctk.CTkEntry(ma_frame, width=80)
        self.ma_threshold.grid(row=7, column=1, sticky="w", padx=10, pady=2)
        self.ma_threshold.insert(0, "0")

        current_row += 1

        # MACD
        macd_frame = Ctk.CTkFrame(indicators_scrollable)
        macd_frame.grid(row=current_row, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        macd_frame.grid_columnconfigure(0, weight=1)
        macd_frame.grid_columnconfigure(1, weight=1)

        Ctk.CTkLabel(macd_frame, text="MACD", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, sticky="w", padx=10, pady=(10, 5))
        Ctk.CTkLabel(macd_frame, text="Active:").grid(row=1, column=0, sticky="w", padx=10, pady=2)
        self.macd_active = Ctk.CTkSwitch(macd_frame, text="")
        self.macd_active.grid(row=1, column=1, sticky="w", padx=10, pady=2)

        Ctk.CTkLabel(macd_frame, text="Fast Period:").grid(row=2, column=0, sticky="w", padx=10, pady=2)
        self.macd_fast = Ctk.CTkEntry(macd_frame, width=80)
        self.macd_fast.grid(row=2, column=1, sticky="w", padx=10, pady=2)
        self.macd_fast.insert(0, "12")

        Ctk.CTkLabel(macd_frame, text="Slow Period:").grid(row=3, column=0, sticky="w", padx=10, pady=2)
        self.macd_slow = Ctk.CTkEntry(macd_frame, width=80)
        self.macd_slow.grid(row=3, column=1, sticky="w", padx=10, pady=2)
        self.macd_slow.insert(0, "26")

        Ctk.CTkLabel(macd_frame, text="Signal Period:").grid(row=4, column=0, sticky="w", padx=10, pady=2)
        self.macd_signal = Ctk.CTkEntry(macd_frame, width=80)
        self.macd_signal.grid(row=4, column=1, sticky="w", padx=10, pady=2)
        self.macd_signal.insert(0, "9")

        Ctk.CTkLabel(macd_frame, text="Source:").grid(row=5, column=0, sticky="w", padx=10, pady=2)
        self.macd_source = Ctk.CTkComboBox(macd_frame, values=["Close", "Open", "High", "Low", "HL2", "HLC3", "OHLC4"])
        self.macd_source.grid(row=5, column=1, sticky="w", padx=10, pady=2)

        Ctk.CTkLabel(macd_frame, text="Condition:").grid(row=6, column=0, sticky="w", padx=10, pady=2)
        self.macd_condition = Ctk.CTkComboBox(macd_frame, values=[
            "MACD Crossing Above Signal", "MACD Crossing Below Signal",
            "MACD Above Zero", "MACD Below Zero", 
            "MACD Crossing Above Zero", "MACD Crossing Below Zero",
            "Histogram Increasing", "Histogram Decreasing",
            "Histogram Positive", "Histogram Negative",
            "Bullish Divergence", "Bearish Divergence"
        ])
        self.macd_condition.grid(row=6, column=1, sticky="w", padx=10, pady=2)

        current_row += 1

        # ADX
        adx_frame = Ctk.CTkFrame(indicators_scrollable)
        adx_frame.grid(row=current_row, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        adx_frame.grid_columnconfigure(0, weight=1)
        adx_frame.grid_columnconfigure(1, weight=1)

        Ctk.CTkLabel(adx_frame, text="ADX", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, sticky="w", padx=10, pady=(10, 5))
        Ctk.CTkLabel(adx_frame, text="Active:").grid(row=1, column=0, sticky="w", padx=10, pady=2)
        self.adx_active = Ctk.CTkSwitch(adx_frame, text="")
        self.adx_active.grid(row=1, column=1, sticky="w", padx=10, pady=2)

        Ctk.CTkLabel(adx_frame, text="Period:").grid(row=2, column=0, sticky="w", padx=10, pady=2)
        self.adx_period = Ctk.CTkEntry(adx_frame, width=80)
        self.adx_period.grid(row=2, column=1, sticky="w", padx=10, pady=2)
        self.adx_period.insert(0, "14")

        Ctk.CTkLabel(adx_frame, text="Threshold:").grid(row=3, column=0, sticky="w", padx=10, pady=2)
        self.adx_threshold = Ctk.CTkEntry(adx_frame, width=80)
        self.adx_threshold.grid(row=3, column=1, sticky="w", padx=10, pady=2)
        self.adx_threshold.insert(0, "25")

        Ctk.CTkLabel(adx_frame, text="Condition:").grid(row=4, column=0, sticky="w", padx=10, pady=2)
        self.adx_condition = Ctk.CTkComboBox(adx_frame, values=[
            "ADX Above Threshold", "ADX Below Threshold",
            "ADX Rising", "ADX Falling",
            "+DI Crossing Above -DI", "+DI Crossing Below -DI",
            "+DI Above -DI", "-DI Above +DI"
        ])
        self.adx_condition.grid(row=4, column=1, sticky="w", padx=10, pady=2)

        current_row += 1

        # Volume
        volume_frame = Ctk.CTkFrame(indicators_scrollable)
        volume_frame.grid(row=current_row, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        volume_frame.grid_columnconfigure(0, weight=1)
        volume_frame.grid_columnconfigure(1, weight=1)

        Ctk.CTkLabel(volume_frame, text="Volume", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, sticky="w", padx=10, pady=(10, 5))
        Ctk.CTkLabel(volume_frame, text="Active:").grid(row=1, column=0, sticky="w", padx=10, pady=2)
        self.volume_active = Ctk.CTkSwitch(volume_frame, text="")
        self.volume_active.grid(row=1, column=1, sticky="w", padx=10, pady=2)

        Ctk.CTkLabel(volume_frame, text="Period:").grid(row=2, column=0, sticky="w", padx=10, pady=2)
        self.volume_period = Ctk.CTkEntry(volume_frame, width=80)
        self.volume_period.grid(row=2, column=1, sticky="w", padx=10, pady=2)
        self.volume_period.insert(0, "20")

        Ctk.CTkLabel(volume_frame, text="Threshold (%):").grid(row=3, column=0, sticky="w", padx=10, pady=2)
        self.volume_threshold = Ctk.CTkEntry(volume_frame, width=80)
        self.volume_threshold.grid(row=3, column=1, sticky="w", padx=10, pady=2)
        self.volume_threshold.insert(0, "150")

        Ctk.CTkLabel(volume_frame, text="Condition:").grid(row=4, column=0, sticky="w", padx=10, pady=2)
        self.volume_condition = Ctk.CTkComboBox(volume_frame, values=[
            "Above Average", "Below Average",
            "Increasing", "Decreasing",
            "Spike (% of Avg)", "Declining (% of Avg)",
            "Bullish Volume (Green Candle)", "Bearish Volume (Red Candle)"
        ])
        self.volume_condition.grid(row=4, column=1, sticky="w", padx=10, pady=2)

        current_row += 1

        # Super-trend
        supertrend_frame = Ctk.CTkFrame(indicators_scrollable)
        supertrend_frame.grid(row=current_row, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        supertrend_frame.grid_columnconfigure(0, weight=1)
        supertrend_frame.grid_columnconfigure(1, weight=1)

        Ctk.CTkLabel(supertrend_frame, text="Super-trend", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, sticky="w", padx=10, pady=(10, 5))
        Ctk.CTkLabel(supertrend_frame, text="Active:").grid(row=1, column=0, sticky="w", padx=10, pady=2)
        self.supertrend_active = Ctk.CTkSwitch(supertrend_frame, text="")
        self.supertrend_active.grid(row=1, column=1, sticky="w", padx=10, pady=2)

        Ctk.CTkLabel(supertrend_frame, text="Period:").grid(row=2, column=0, sticky="w", padx=10, pady=2)
        self.supertrend_period = Ctk.CTkEntry(supertrend_frame, width=80)
        self.supertrend_period.grid(row=2, column=1, sticky="w", padx=10, pady=2)
        self.supertrend_period.insert(0, "10")

        Ctk.CTkLabel(supertrend_frame, text="Multiplier:").grid(row=3, column=0, sticky="w", padx=10, pady=2)
        self.supertrend_multiplier = Ctk.CTkEntry(supertrend_frame, width=80)
        self.supertrend_multiplier.grid(row=3, column=1, sticky="w", padx=10, pady=2)
        self.supertrend_multiplier.insert(0, "3")

        Ctk.CTkLabel(supertrend_frame, text="Condition:").grid(row=4, column=0, sticky="w", padx=10, pady=2)
        self.supertrend_condition = Ctk.CTkComboBox(supertrend_frame, values=[
            "Bullish (Green)", "Bearish (Red)",
            "Bullish Crossover", "Bearish Crossover",
            "Price Above Super-trend", "Price Below Super-trend"
        ])
        self.supertrend_condition.grid(row=4, column=1, sticky="w", padx=10, pady=2)

        current_row += 1

        
        # Fibonacci
        fibonacci_frame = Ctk.CTkFrame(indicators_scrollable)
        fibonacci_frame.grid(row=current_row, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        fibonacci_frame.grid_columnconfigure(0, weight=1)
        fibonacci_frame.grid_columnconfigure(1, weight=1)

        Ctk.CTkLabel(fibonacci_frame, text="Fibonacci", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, sticky="w", padx=10, pady=(10, 5))
        Ctk.CTkLabel(fibonacci_frame, text="Active:").grid(row=1, column=0, sticky="w", padx=10, pady=2)
        self.fibonacci_active = Ctk.CTkSwitch(fibonacci_frame, text="")
        self.fibonacci_active.grid(row=1, column=1, sticky="w", padx=10, pady=2)

        Ctk.CTkLabel(fibonacci_frame, text="Standard levels:").grid(row=2, column=0, sticky="w", padx=10, pady=2)
        self.fibonacci_levels = Ctk.CTkSwitch(fibonacci_frame, text="")
        self.fibonacci_levels.grid(row=2, column=1, sticky="w", padx=10, pady=2)
        self.fibonacci_levels.select()  # Default to standard levels enabled

        current_row += 1

        # Up Trend
        uptrend_frame = Ctk.CTkFrame(indicators_scrollable)
        uptrend_frame.grid(row=current_row, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        uptrend_frame.grid_columnconfigure(0, weight=1)
        uptrend_frame.grid_columnconfigure(1, weight=1)

        Ctk.CTkLabel(uptrend_frame, text="Up Trend", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, sticky="w", padx=10, pady=(10, 5))
        Ctk.CTkLabel(uptrend_frame, text="Active:").grid(row=1, column=0, sticky="w", padx=10, pady=2)
        self.uptrend_active = Ctk.CTkSwitch(uptrend_frame, text="")
        self.uptrend_active.grid(row=1, column=1, sticky="w", padx=10, pady=2)

        Ctk.CTkLabel(uptrend_frame, text="Time Frame:").grid(row=2, column=0, sticky="w", padx=10, pady=2)
        self.uptrend_timeframe = Ctk.CTkComboBox(uptrend_frame, values=[
            "1m", "5m", "15m", "30m", "1h", "4h", "1d", "1w"
        ])
        self.uptrend_timeframe.grid(row=2, column=1, sticky="w", padx=10, pady=2)
        self.uptrend_timeframe.set("1h")  # Default value

        Ctk.CTkLabel(uptrend_frame, text="Number of Candles:").grid(row=3, column=0, sticky="w", padx=10, pady=2)
        self.uptrend_candles = Ctk.CTkEntry(uptrend_frame, width=80)
        self.uptrend_candles.grid(row=3, column=1, sticky="w", padx=10, pady=2)
        self.uptrend_candles.insert(0, "5")  # Default value

        current_row += 1

        # Down Trend
        downtrend_frame = Ctk.CTkFrame(indicators_scrollable)
        downtrend_frame.grid(row=current_row, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        downtrend_frame.grid_columnconfigure(0, weight=1)
        downtrend_frame.grid_columnconfigure(1, weight=1)

        Ctk.CTkLabel(downtrend_frame, text="Down Trend", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, sticky="w", padx=10, pady=(10, 5))
        Ctk.CTkLabel(downtrend_frame, text="Active:").grid(row=1, column=0, sticky="w", padx=10, pady=2)
        self.downtrend_active = Ctk.CTkSwitch(downtrend_frame, text="")
        self.downtrend_active.grid(row=1, column=1, sticky="w", padx=10, pady=2)

        Ctk.CTkLabel(downtrend_frame, text="Time Frame:").grid(row=2, column=0, sticky="w", padx=10, pady=2)
        self.downtrend_timeframe = Ctk.CTkComboBox(downtrend_frame, values=[
            "1m", "5m", "15m", "30m", "1h", "4h", "1d", "1w"
        ])
        self.downtrend_timeframe.grid(row=2, column=1, sticky="w", padx=10, pady=2)
        self.downtrend_timeframe.set("1h")  # Default value

        Ctk.CTkLabel(downtrend_frame, text="Number of Candles:").grid(row=3, column=0, sticky="w", padx=10, pady=2)
        self.downtrend_candles = Ctk.CTkEntry(downtrend_frame, width=80)
        self.downtrend_candles.grid(row=3, column=1, sticky="w", padx=10, pady=2)
        self.downtrend_candles.insert(0, "5")  # Default value

        current_row += 1


        # --- Entry Tab ---
        entry_tab = self.tabview.tab("Entry")

        # Main frame for entry conditions
        entry_frame = Ctk.CTkFrame(entry_tab)
        entry_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Title
        Ctk.CTkLabel(entry_frame, text="Entry Conditions Configuration", 
                    font=("Arial", 16, "bold")).pack(pady=(10, 20))

        # Create scrollable frame for conditions
        entry_scrollable = Ctk.CTkScrollableFrame(entry_frame)
        entry_scrollable.pack(fill="both", expand=True, padx=10, pady=10)
        entry_scrollable.grid_columnconfigure(0, weight=1)
        entry_scrollable.grid_columnconfigure(1, weight=1)

        # Instructions
        instructions = Ctk.CTkLabel(entry_scrollable, 
                                text="Configure how indicators combine for entry signals. Select indicators, " + 
                                        "logical operators, and sequence requirements.")
        instructions.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=(5, 15))

        # Condition Builder
        condition_frame = Ctk.CTkFrame(entry_scrollable)
        condition_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=5, pady=10)
        condition_frame.grid_columnconfigure(0, weight=1)
        condition_frame.grid_columnconfigure(1, weight=1)

        Ctk.CTkLabel(condition_frame, text="Entry Condition Builder", 
                    font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, sticky="w", padx=10, pady=(10, 15))

        # Logic selection
        Ctk.CTkLabel(condition_frame, text="Default Logic:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.entry_default_logic = Ctk.CTkComboBox(condition_frame, values=["AND", "OR"])
        self.entry_default_logic.grid(row=1, column=1, sticky="w", padx=10, pady=5)
        self.entry_default_logic.set("AND")

        # Sequence toggle
        Ctk.CTkLabel(condition_frame, text="Use Sequence:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.entry_use_sequence = Ctk.CTkSwitch(condition_frame, text="")
        self.entry_use_sequence.grid(row=2, column=1, sticky="w", padx=10, pady=5)

        # Conditions list
        conditions_list_frame = Ctk.CTkFrame(entry_scrollable)
        conditions_list_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=5, pady=10)
        conditions_list_frame.grid_columnconfigure(0, weight=3)
        conditions_list_frame.grid_columnconfigure(1, weight=1)
        conditions_list_frame.grid_columnconfigure(2, weight=1)
        conditions_list_frame.grid_columnconfigure(3, weight=1)

        Ctk.CTkLabel(conditions_list_frame, text="Indicators", 
                    font=("Arial", 12, "bold")).grid(row=0, column=0, sticky="w", padx=10, pady=5)
        Ctk.CTkLabel(conditions_list_frame, text="Logic", 
                    font=("Arial", 12, "bold")).grid(row=0, column=1, sticky="w", padx=10, pady=5)
        Ctk.CTkLabel(conditions_list_frame, text="NOT", 
                    font=("Arial", 12, "bold")).grid(row=0, column=2, sticky="w", padx=10, pady=5)
        Ctk.CTkLabel(conditions_list_frame, text="Seq #", 
                    font=("Arial", 12, "bold")).grid(row=0, column=3, sticky="w", padx=10, pady=5)

        # List of all indicators for selection
        indicators = [
            "Bollinger Bands", "RSI", "Stochastic RSI", "Moving Averages", 
            "MACD", "ADX", "Volume", "Super-trend", "Fibonacci", 
            "Up Trend", "Down Trend"
        ]

        # Create entry rows for each indicator
        self.entry_conditions = []  # Store references to all condition widgets
        for i, indicator in enumerate(indicators):
            row = i + 1
            
            # Indicator checkbox
            indicator_var = Ctk.CTkCheckBox(conditions_list_frame, text=indicator)
            indicator_var.grid(row=row, column=0, sticky="w", padx=10, pady=3)
            
            # Logic dropdown (AND/OR)
            logic_var = Ctk.CTkComboBox(conditions_list_frame, values=["AND", "OR"], width=80)
            logic_var.grid(row=row, column=1, sticky="w", padx=10, pady=3)
            logic_var.set("AND")
            
            # NOT checkbox
            not_var = Ctk.CTkCheckBox(conditions_list_frame, text="")
            not_var.grid(row=row, column=2, sticky="w", padx=10, pady=3)
            
            # Sequence number entry
            seq_var = Ctk.CTkEntry(conditions_list_frame, width=60)
            seq_var.grid(row=row, column=3, sticky="w", padx=10, pady=3)
            seq_var.insert(0, str(row))  # Default sequential order
            
            # Store references
            self.entry_conditions.append({
                "indicator": indicator,
                "checkbox": indicator_var,
                "logic": logic_var,
                "not": not_var,
                "sequence": seq_var
            })

        # Buttons for managing conditions
        buttons_frame = Ctk.CTkFrame(entry_scrollable)
        buttons_frame.grid(row=3, column=0, columnspan=2, sticky="ew", padx=5, pady=10)
        buttons_frame.grid_columnconfigure(0, weight=1)
        buttons_frame.grid_columnconfigure(1, weight=1)
        buttons_frame.grid_columnconfigure(2, weight=1)

        reset_btn = Ctk.CTkButton(buttons_frame, text="Reset All", 
                                command=lambda: self.reset_entry_conditions())
        reset_btn.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        test_btn = Ctk.CTkButton(buttons_frame, text="Test Conditions", 
                                command=lambda: self.test_entry_conditions())
        test_btn.grid(row=0, column=1, sticky="ew", padx=10, pady=10)

        save_btn = Ctk.CTkButton(buttons_frame, text="Save Conditions", 
                                command=lambda: self.save_entry_conditions())
        save_btn.grid(row=0, column=2, sticky="ew", padx=10, pady=10)

        # Preview frame
        preview_frame = Ctk.CTkFrame(entry_scrollable)
        preview_frame.grid(row=4, column=0, columnspan=2, sticky="ew", padx=5, pady=10)

        Ctk.CTkLabel(preview_frame, text="Condition Preview", 
                    font=("Arial", 14, "bold")).pack(pady=(10, 5), padx=10, anchor="w")

        self.condition_preview = Ctk.CTkTextbox(preview_frame, height=100)
        self.condition_preview.pack(fill="both", expand=True, padx=10, pady=(5, 10))
        self.condition_preview.insert("1.0", "No conditions configured yet. Select indicators and configure logic above.")
        self.condition_preview.configure(state="disabled")
"""