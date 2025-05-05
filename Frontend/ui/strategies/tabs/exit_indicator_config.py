import customtkinter as Ctk
from tkinter import messagebox

class IndicatorConfigDialog:
    """Dialog for configuring indicator parameters"""
    def __init__(self, parent, indicator_type):
        self.result = None
        self.dialog = Ctk.CTkToplevel(parent)
        self.dialog.title(f"Configure {indicator_type}")
        self.dialog.transient(parent)
        self.dialog.wait_visibility()  # Ensure the window is visible before grabbing focus
        self.dialog.grab_set()

        # Set fixed size for the dialog
        dialog_width = 400
        dialog_height = 500  # Fixed height that should accommodate most indicators
        
        # Center the dialog on the screen
        x = (self.dialog.winfo_screenwidth() // 2) - (dialog_width // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (dialog_height // 2)
        self.dialog.geometry(f"{dialog_width}x{dialog_height}+{x}+{y}")
        
        self.indicator_type = indicator_type
        self.dialog.grid_columnconfigure(0, weight=1)
        self.dialog.grid_columnconfigure(1, weight=2)
        
        # Title
        title_label = Ctk.CTkLabel(
            self.dialog, 
            text=f"Configure {indicator_type}", 
            font=("Helvetica", 16, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 10), sticky="ew")
        
        # Parameters dictionary to store all parameter inputs
        self.param_entries = {}
        
        # Different parameters based on indicator type
        current_row = 1
        
        if indicator_type == "Bollinger Bands":
            # Period parameter
            Ctk.CTkLabel(self.dialog, text="Period:").grid(row=current_row, column=0, padx=10, pady=5, sticky="e")
            period_entry = Ctk.CTkEntry(self.dialog)
            period_entry.insert(0, "20")  # Default value
            period_entry.grid(row=current_row, column=1, padx=10, pady=5, sticky="ew")
            self.param_entries["period"] = period_entry
            current_row += 1
            
            # Standard Deviation parameter
            Ctk.CTkLabel(self.dialog, text="Standard Deviation:").grid(row=current_row, column=0, padx=10, pady=5, sticky="e")
            std_dev_entry = Ctk.CTkEntry(self.dialog)
            std_dev_entry.insert(0, "2")  # Default value
            std_dev_entry.grid(row=current_row, column=1, padx=10, pady=5, sticky="ew")
            self.param_entries["std_dev"] = std_dev_entry
            current_row += 1
            
            # Source parameter
            Ctk.CTkLabel(self.dialog, text="Source:").grid(row=current_row, column=0, padx=10, pady=5, sticky="e")
            source_combo = Ctk.CTkComboBox(self.dialog, values=["Close", "Open", "High", "Low", "HL2", "HLC3", "OHLC4"])
            source_combo.set("Close")  # Default value
            source_combo.grid(row=current_row, column=1, padx=10, pady=5, sticky="ew")
            self.param_entries["source"] = source_combo
            current_row += 1
            
            # Threshold parameter
            Ctk.CTkLabel(self.dialog, text="MBB Threshold (%):").grid(row=current_row, column=0, padx=10, pady=5, sticky="e")
            threshold_entry = Ctk.CTkEntry(self.dialog)
            threshold_entry.insert(0, "0.3")  # Default value
            threshold_entry.grid(row=current_row, column=1, padx=10, pady=5, sticky="ew")
            self.param_entries["threshold"] = threshold_entry
            current_row += 1
            
        elif indicator_type == "RSI":
            Ctk.CTkLabel(self.dialog, text="Period:").grid(row=current_row, column=0, padx=10, pady=5, sticky="e")
            period_entry = Ctk.CTkEntry(self.dialog)
            period_entry.insert(0, "14")
            period_entry.grid(row=current_row, column=1, padx=10, pady=5, sticky="ew")
            self.param_entries["period"] = period_entry
            current_row += 1

            Ctk.CTkLabel(self.dialog, text="Overbought Level:").grid(row=current_row, column=0, padx=10, pady=5, sticky="e")
            overbought_entry = Ctk.CTkEntry(self.dialog)
            overbought_entry.insert(0, "70")
            overbought_entry.grid(row=current_row, column=1, padx=10, pady=5, sticky="ew")
            self.param_entries["overbought_level"] = overbought_entry
            current_row += 1

            Ctk.CTkLabel(self.dialog, text="Oversold Level:").grid(row=current_row, column=0, padx=10, pady=5, sticky="e")
            oversold_entry = Ctk.CTkEntry(self.dialog)
            oversold_entry.insert(0, "30")
            oversold_entry.grid(row=current_row, column=1, padx=10, pady=5, sticky="ew")
            self.param_entries["oversold_level"] = oversold_entry
            current_row += 1

            Ctk.CTkLabel(self.dialog, text="Source:").grid(row=current_row, column=0, padx=10, pady=5, sticky="e")
            source_combo = Ctk.CTkComboBox(self.dialog, values=["Close", "Open", "High", "Low", "HL2", "HLC3", "OHLC4"])
            source_combo.set("Close")
            source_combo.grid(row=current_row, column=1, padx=10, pady=5, sticky="ew")
            self.param_entries["source"] = source_combo
            current_row += 1

            Ctk.CTkLabel(self.dialog, text="Condition:").grid(row=current_row, column=0, padx=10, pady=5, sticky="e")
            condition_combo = Ctk.CTkComboBox(self.dialog, values=["Crossing Above Oversold", "Crossing Below Overbought", 
                                                                "Above Specific Value", "Below Specific Value", "Divergence"])
            condition_combo.set("Crossing Above Oversold")
            condition_combo.grid(row=current_row, column=1, padx=10, pady=5, sticky="ew")
            self.param_entries["condition"] = condition_combo
            current_row += 1

            Ctk.CTkLabel(self.dialog, text="Specific Value:").grid(row=current_row, column=0, padx=10, pady=5, sticky="e")
            specific_value_entry = Ctk.CTkEntry(self.dialog)
            specific_value_entry.insert(0, "50")
            specific_value_entry.grid(row=current_row, column=1, padx=10, pady=5, sticky="ew")
            self.param_entries["specific_value"] = specific_value_entry
            current_row += 1

                    
        elif indicator_type == "Moving Averages":
            Ctk.CTkLabel(self.dialog, text="MA Type:").grid(row=current_row, column=0, padx=10, pady=5, sticky="e")
            ma_type_combo = Ctk.CTkComboBox(self.dialog, values=["Simple", "Exponential", "Weighted", "Hull"])
            ma_type_combo.set("Simple")
            ma_type_combo.grid(row=current_row, column=1, padx=10, pady=5, sticky="ew")
            self.param_entries["ma_type"] = ma_type_combo
            current_row += 1

            Ctk.CTkLabel(self.dialog, text="Period 1:").grid(row=current_row, column=0, padx=10, pady=5, sticky="e")
            ma_period1_entry = Ctk.CTkEntry(self.dialog)
            ma_period1_entry.insert(0, "20")
            ma_period1_entry.grid(row=current_row, column=1, padx=10, pady=5, sticky="ew")
            self.param_entries["ma_period1"] = ma_period1_entry
            current_row += 1

            Ctk.CTkLabel(self.dialog, text="Period 2:").grid(row=current_row, column=0, padx=10, pady=5, sticky="e")
            ma_period2_entry = Ctk.CTkEntry(self.dialog)
            ma_period2_entry.insert(0, "50")
            ma_period2_entry.grid(row=current_row, column=1, padx=10, pady=5, sticky="ew")
            self.param_entries["ma_period2"] = ma_period2_entry
            current_row += 1

            Ctk.CTkLabel(self.dialog, text="Source:").grid(row=current_row, column=0, padx=10, pady=5, sticky="e")
            ma_source_combo = Ctk.CTkComboBox(self.dialog, values=["Close", "Open", "High", "Low", "HL2", "HLC3", "OHLC4"])
            ma_source_combo.set("Close")
            ma_source_combo.grid(row=current_row, column=1, padx=10, pady=5, sticky="ew")
            self.param_entries["ma_source"] = ma_source_combo
            current_row += 1

            Ctk.CTkLabel(self.dialog, text="Condition:").grid(row=current_row, column=0, padx=10, pady=5, sticky="e")
            ma_condition_combo = Ctk.CTkComboBox(self.dialog, values=[
                "Price Above MA", "Price Below MA", 
                "Price Crossing Above MA", "Price Crossing Below MA",
                "Fast MA Crossing Above Slow MA", "Fast MA Crossing Below Slow MA",
                "MA Slope Up", "MA Slope Down"
            ])
            ma_condition_combo.set("Price Above MA")
            ma_condition_combo.grid(row=current_row, column=1, padx=10, pady=5, sticky="ew")
            self.param_entries["ma_condition"] = ma_condition_combo
            current_row += 1

            Ctk.CTkLabel(self.dialog, text="Threshold:").grid(row=current_row, column=0, padx=10, pady=5, sticky="e")
            ma_threshold_entry = Ctk.CTkEntry(self.dialog)
            ma_threshold_entry.insert(0, "0")
            ma_threshold_entry.grid(row=current_row, column=1, padx=10, pady=5, sticky="ew")
            self.param_entries["ma_threshold"] = ma_threshold_entry
            current_row += 1


        elif indicator_type == "MACD":
            Ctk.CTkLabel(self.dialog, text="Fast Period:").grid(row=current_row, column=0, padx=10, pady=5, sticky="e")
            macd_fast_entry = Ctk.CTkEntry(self.dialog)
            macd_fast_entry.insert(0, "12")
            macd_fast_entry.grid(row=current_row, column=1, padx=10, pady=5, sticky="ew")
            self.param_entries["fast_period"] = macd_fast_entry
            current_row += 1

            Ctk.CTkLabel(self.dialog, text="Slow Period:").grid(row=current_row, column=0, padx=10, pady=5, sticky="e")
            macd_slow_entry = Ctk.CTkEntry(self.dialog)
            macd_slow_entry.insert(0, "26")
            macd_slow_entry.grid(row=current_row, column=1, padx=10, pady=5, sticky="ew")
            self.param_entries["slow_period"] = macd_slow_entry
            current_row += 1

            Ctk.CTkLabel(self.dialog, text="Signal Period:").grid(row=current_row, column=0, padx=10, pady=5, sticky="e")
            macd_signal_entry = Ctk.CTkEntry(self.dialog)
            macd_signal_entry.insert(0, "9")
            macd_signal_entry.grid(row=current_row, column=1, padx=10, pady=5, sticky="ew")
            self.param_entries["signal_period"] = macd_signal_entry
            current_row += 1

            Ctk.CTkLabel(self.dialog, text="Source:").grid(row=current_row, column=0, padx=10, pady=5, sticky="e")
            macd_source_combo = Ctk.CTkComboBox(self.dialog, values=["Close", "Open", "High", "Low", "HL2", "HLC3", "OHLC4"])
            macd_source_combo.set("Close")
            macd_source_combo.grid(row=current_row, column=1, padx=10, pady=5, sticky="ew")
            self.param_entries["source"] = macd_source_combo
            current_row += 1

            Ctk.CTkLabel(self.dialog, text="Condition:").grid(row=current_row, column=0, padx=10, pady=5, sticky="e")
            macd_condition_combo = Ctk.CTkComboBox(self.dialog, values=[
                "MACD Crossing Above Signal", "MACD Crossing Below Signal",
                "MACD Above Zero", "MACD Below Zero",
                "MACD Crossing Above Zero", "MACD Crossing Below Zero",
                "Histogram Increasing", "Histogram Decreasing",
                "Histogram Positive", "Histogram Negative",
                "Bullish Divergence", "Bearish Divergence"
            ])
            macd_condition_combo.set("MACD Crossing Above Signal")
            macd_condition_combo.grid(row=current_row, column=1, padx=10, pady=5, sticky="ew")
            self.param_entries["condition"] = macd_condition_combo
            current_row += 1

        elif indicator_type == "Super-trend":
            Ctk.CTkLabel(self.dialog, text="Factor:").grid(row=current_row, column=0, padx=10, pady=10, sticky="e")
            factor_entry = Ctk.CTkEntry(self.dialog)
            factor_entry.insert(0, "3")  # Default value
            factor_entry.grid(row=current_row, column=1, padx=10, pady=10, sticky="ew")
            self.param_entries["factor"] = factor_entry
            current_row += 1
        
        elif indicator_type == "Stochastic RSI":
            Ctk.CTkLabel(self.dialog, text="K Period:").grid(row=current_row, column=0, padx=10, pady=5, sticky="e")
            k_period_entry = Ctk.CTkEntry(self.dialog)
            k_period_entry.insert(0, "14")
            k_period_entry.grid(row=current_row, column=1, padx=10, pady=5, sticky="ew")
            self.param_entries["k_period"] = k_period_entry
            current_row += 1
            
            Ctk.CTkLabel(self.dialog, text="D Period:").grid(row=current_row, column=0, padx=10, pady=5, sticky="e")
            d_period_entry = Ctk.CTkEntry(self.dialog)
            d_period_entry.insert(0, "3")
            d_period_entry.grid(row=current_row, column=1, padx=10, pady=5, sticky="ew")
            self.param_entries["d_period"] = d_period_entry
            current_row += 1
            
            Ctk.CTkLabel(self.dialog, text="RSI Period:").grid(row=current_row, column=0, padx=10, pady=5, sticky="e")
            rsi_period_entry = Ctk.CTkEntry(self.dialog)
            rsi_period_entry.insert(0, "14")
            rsi_period_entry.grid(row=current_row, column=1, padx=10, pady=5, sticky="ew")
            self.param_entries["rsi_period"] = rsi_period_entry
            current_row += 1
            
            Ctk.CTkLabel(self.dialog, text="Stochastic Period:").grid(row=current_row, column=0, padx=10, pady=5, sticky="e")
            stoch_period_entry = Ctk.CTkEntry(self.dialog)
            stoch_period_entry.insert(0, "14")
            stoch_period_entry.grid(row=current_row, column=1, padx=10, pady=5, sticky="ew")
            self.param_entries["stoch_period"] = stoch_period_entry
            current_row += 1

        elif indicator_type == "ADX":
            Ctk.CTkLabel(self.dialog, text="Period:").grid(row=current_row, column=0, padx=10, pady=5, sticky="e")
            period_entry = Ctk.CTkEntry(self.dialog)
            period_entry.insert(0, "14")
            period_entry.grid(row=current_row, column=1, padx=10, pady=5, sticky="ew")
            self.param_entries["period"] = period_entry
            current_row += 1
            
            Ctk.CTkLabel(self.dialog, text="Threshold:").grid(row=current_row, column=0, padx=10, pady=5, sticky="e")
            threshold_entry = Ctk.CTkEntry(self.dialog)
            threshold_entry.insert(0, "25")
            threshold_entry.grid(row=current_row, column=1, padx=10, pady=5, sticky="ew")
            self.param_entries["threshold"] = threshold_entry
            current_row += 1

        elif indicator_type == "Volume":
            Ctk.CTkLabel(self.dialog, text="Period:").grid(row=current_row, column=0, padx=10, pady=5, sticky="e")
            period_entry = Ctk.CTkEntry(self.dialog)
            period_entry.insert(0, "20")
            period_entry.grid(row=current_row, column=1, padx=10, pady=5, sticky="ew")
            self.param_entries["period"] = period_entry
            current_row += 1
            
            Ctk.CTkLabel(self.dialog, text="Multiplier:").grid(row=current_row, column=0, padx=10, pady=5, sticky="e")
            multiplier_entry = Ctk.CTkEntry(self.dialog)
            multiplier_entry.insert(0, "2.0")
            multiplier_entry.grid(row=current_row, column=1, padx=10, pady=5, sticky="ew")
            self.param_entries["multiplier"] = multiplier_entry
            current_row += 1

        elif indicator_type == "Fibonacci":
            Ctk.CTkLabel(self.dialog, text="Retracement Level:").grid(row=current_row, column=0, padx=10, pady=5, sticky="e")
            level_combo = Ctk.CTkComboBox(self.dialog, values=["0.236", "0.382", "0.5", "0.618", "0.786"])
            level_combo.set("0.618")
            level_combo.grid(row=current_row, column=1, padx=10, pady=5, sticky="ew")
            self.param_entries["level"] = level_combo
            current_row += 1

        if indicator_type == "Up Trend":
            # Number of candles parameter
            Ctk.CTkLabel(self.dialog, text="Number of Candles:").grid(row=current_row, column=0, padx=10, pady=5, sticky="e")
            candles_entry = Ctk.CTkEntry(self.dialog)
            candles_entry.insert(0, "14")  # Default value
            candles_entry.grid(row=current_row, column=1, padx=10, pady=5, sticky="ew")
            self.param_entries["candles"] = candles_entry
            current_row += 1

            # Timeframe parameter
            Ctk.CTkLabel(self.dialog, text="Timeframe:").grid(row=current_row, column=0, padx=10, pady=5, sticky="e")
            timeframe_combo = Ctk.CTkComboBox(self.dialog, values=["1m", "5m", "15m", "30m", "1h", "4h", "1d", "1w"])
            timeframe_combo.set("1h")  # Default value
            timeframe_combo.grid(row=current_row, column=1, padx=10, pady=5, sticky="ew")
            self.param_entries["timeframe"] = timeframe_combo
            current_row += 1

            # Source parameter
            Ctk.CTkLabel(self.dialog, text="Source:").grid(row=current_row, column=0, padx=10, pady=5, sticky="e")
            source_combo = Ctk.CTkComboBox(self.dialog, values=["Close", "Open", "High", "Low", "HL2", "HLC3", "OHLC4"])
            source_combo.set("Close")  # Default value
            source_combo.grid(row=current_row, column=1, padx=10, pady=5, sticky="ew")
            self.param_entries["source"] = source_combo
            current_row += 1

            # Condition parameter
            Ctk.CTkLabel(self.dialog, text="Condition:").grid(row=current_row, column=0, padx=10, pady=5, sticky="e")
            condition_values = ["Higher Highs", "Higher Lows", "Both"]
            condition_combo = Ctk.CTkComboBox(self.dialog, values=condition_values)
            condition_combo.set(condition_values[0])  # Default value
            condition_combo.grid(row=current_row, column=1, padx=10, pady=5, sticky="ew")
            self.param_entries["condition"] = condition_combo
            current_row += 1

        elif indicator_type == "Down Trend":
            # Number of candles parameter
            Ctk.CTkLabel(self.dialog, text="Number of Candles:").grid(row=current_row, column=0, padx=10, pady=5, sticky="e")
            candles_entry = Ctk.CTkEntry(self.dialog)
            candles_entry.insert(0, "14")  # Default value
            candles_entry.grid(row=current_row, column=1, padx=10, pady=5, sticky="ew")
            self.param_entries["candles"] = candles_entry
            current_row += 1

            # Timeframe parameter
            Ctk.CTkLabel(self.dialog, text="Timeframe:").grid(row=current_row, column=0, padx=10, pady=5, sticky="e")
            timeframe_combo = Ctk.CTkComboBox(self.dialog, values=["1m", "5m", "15m", "30m", "1h", "4h", "1d", "1w"])
            timeframe_combo.set("1h")  # Default value
            timeframe_combo.grid(row=current_row, column=1, padx=10, pady=5, sticky="ew")
            self.param_entries["timeframe"] = timeframe_combo
            current_row += 1

            # Source parameter
            Ctk.CTkLabel(self.dialog, text="Source:").grid(row=current_row, column=0, padx=10, pady=5, sticky="e")
            source_combo = Ctk.CTkComboBox(self.dialog, values=["Close", "Open", "High", "Low", "HL2", "HLC3", "OHLC4"])
            source_combo.set("Close")  # Default value
            source_combo.grid(row=current_row, column=1, padx=10, pady=5, sticky="ew")
            self.param_entries["source"] = source_combo
            current_row += 1

            # Condition parameter
            Ctk.CTkLabel(self.dialog, text="Condition:").grid(row=current_row, column=0, padx=10, pady=5, sticky="e")
            condition_values = ["Lower Highs", "Lower Lows", "Both"]
            condition_combo = Ctk.CTkComboBox(self.dialog, values=condition_values)
            condition_combo.set(condition_values[0])  # Default value
            condition_combo.grid(row=current_row, column=1, padx=10, pady=5, sticky="ew")
            self.param_entries["condition"] = condition_combo
            current_row += 1

        else:
            # Generic parameter for any other indicator
            Ctk.CTkLabel(self.dialog, text="Value:").grid(row=current_row, column=0, padx=10, pady=10, sticky="e")
            value_entry = Ctk.CTkEntry(self.dialog)
            value_entry.insert(0, "0")  # Default value
            value_entry.grid(row=current_row, column=1, padx=10, pady=10, sticky="ew")
            self.param_entries["value"] = value_entry
            current_row += 1
        
        # Display name for the configured indicator
        Ctk.CTkLabel(self.dialog, text="Display Name:").grid(row=current_row, column=0, padx=10, pady=10, sticky="e")
        self.display_name = Ctk.CTkEntry(self.dialog)
        self.display_name.insert(0, f"{indicator_type}")
        self.display_name.grid(row=current_row, column=1, padx=10, pady=10, sticky="ew")
        current_row += 1
        
        # Buttons
        button_frame = Ctk.CTkFrame(self.dialog)
        button_frame.grid(row=current_row, column=0, columnspan=2, padx=20, pady=20, sticky="ew")
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)
        
        Ctk.CTkButton(
            button_frame, 
            text="Cancel", 
            command=self.cancel
        ).grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        Ctk.CTkButton(
            button_frame, 
            text="OK", 
            command=self.ok
        ).grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        # Adjust dialog size based on content
        self.dialog.update_idletasks()
        # Add some padding
        width = 400
        height = min(self.dialog.winfo_reqheight() + 50, 600)  # Limit max height
        
        # Center the dialog
        x = (self.dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (height // 2)
        self.dialog.geometry(f"{width}x{height}+{x}+{y}")
        
        # Wait for the dialog to close
        parent.wait_window(self.dialog)
    
    def ok(self):
        """Save the configuration and close the dialog"""
        try:
            # Process all parameters with validation
            params = {}
            for param_name, entry in self.param_entries.items():
                # Handle special cases for comboboxes
                if param_name in ["source", "condition", "ma_type", "ma_source", "ma_condition", "level", "timeframe"]:
                    params[param_name] = entry.get()
                else:
                    # For Up Trend and Down Trend, ensure candles is an integer
                    if self.indicator_type in ["Up Trend", "Down Trend"] and param_name == "candles":
                        params[param_name] = int(entry.get())
                    else:
                        # Convert to float for numeric values
                        params[param_name] = float(entry.get())
            
            self.result = {
                "type": self.indicator_type,
                "display_name": self.display_name.get(),
                "parameters": params
            }
            self.dialog.destroy()
        except ValueError as e:
            messagebox.showerror("Invalid Input", "Please enter valid numbers for the parameter fields.")
            
    def cancel(self):
        """Close the dialog without saving"""
        self.dialog.destroy()