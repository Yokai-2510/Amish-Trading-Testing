import customtkinter as Ctk
from tkinter import messagebox

class EntryExitConfigurationsTab:
    def __init__(self, parent):
        self.parent = parent
        
        # Create scrollable frame as the main container
        self.scrollable_frame = Ctk.CTkScrollableFrame(self.parent)
        self.scrollable_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Configure columns in scrollable frame
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        self.scrollable_frame.grid_columnconfigure(1, weight=1)
        
        # Create all widgets
        self._create_widgets()
        
    def _create_widgets(self):
        current_row = 0
        
        # ===== ENTRY CONFIGURATIONS SECTION =====
        entry_title = Ctk.CTkLabel(
            self.scrollable_frame, 
            text="ENTRY CONFIGURATIONS", 
            font=("Roboto", 14, "bold"),
            anchor="center"
        )
        entry_title.grid(row=current_row, column=0, columnspan=2, padx=10, pady=(20, 10), sticky="ew")
        current_row += 1
        
        # Entry Chart Configurations
        Ctk.CTkLabel(self.scrollable_frame, text="Entry Chart Type:").grid(
            row=current_row, column=0, padx=10, pady=10, sticky="w"
        )
        self.entry_chart_type_combobox = Ctk.CTkComboBox(
            self.scrollable_frame, values=["Candle Stick", "Heiken Ashi", "Renko"]
        )
        self.entry_chart_type_combobox.grid(row=current_row, column=1, padx=10, pady=10, sticky="ew")
        current_row += 1
        
        Ctk.CTkLabel(self.scrollable_frame, text="Entry Chart Timeframe:").grid(
            row=current_row, column=0, padx=10, pady=10, sticky="w"
        )
        self.entry_chart_timeframe_combobox = Ctk.CTkComboBox(
            self.scrollable_frame, values=["1m", "2m", "3M", "5M", "10M", "1H", "3H", "1D", "1W", "1M"]
        )
        self.entry_chart_timeframe_combobox.grid(row=current_row, column=1, padx=10, pady=10, sticky="ew")
        current_row += 1
        
        # Create a frame for Exclude Time
        exclude_time_frame = Ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
        exclude_time_frame.grid(row=current_row, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        exclude_time_frame.grid_columnconfigure(0, weight=1)
        exclude_time_frame.grid_columnconfigure(1, weight=1)
        
        # Exclude Time title
        exclude_time_title = Ctk.CTkLabel(
            exclude_time_frame, 
            text="Exclude Time Settings", 
            font=("Roboto", 12, "italic")
        )
        exclude_time_title.grid(row=0, column=0, columnspan=2, padx=10, pady=(5, 5), sticky="w")
        
        # Exclude Time Configuration
        Ctk.CTkLabel(exclude_time_frame, text="Exclude Time From:").grid(
            row=1, column=0, padx=10, pady=5, sticky="w"
        )
        self.exclude_time_from_entry = Ctk.CTkEntry(
            exclude_time_frame, placeholder_text="HH:MM (24-hour format)"
        )
        self.exclude_time_from_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        
        Ctk.CTkLabel(exclude_time_frame, text="Exclude Time To:").grid(
            row=2, column=0, padx=10, pady=5, sticky="w"
        )
        self.exclude_time_to_entry = Ctk.CTkEntry(
            exclude_time_frame, placeholder_text="HH:MM (24-hour format)"
        )
        self.exclude_time_to_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
        current_row += 1
        
        # Separator
        separator = Ctk.CTkFrame(self.scrollable_frame, height=2, fg_color="gray70")
        separator.grid(row=current_row, column=0, columnspan=2, padx=20, pady=10, sticky="ew")
        current_row += 1
        
        # ===== EXIT CONFIGURATIONS SECTION =====
        exit_title = Ctk.CTkLabel(
            self.scrollable_frame, 
            text="EXIT CONFIGURATIONS", 
            font=("Roboto", 14, "bold"),
            anchor="center"
        )
        exit_title.grid(row=current_row, column=0, columnspan=2, padx=10, pady=(20, 10), sticky="ew")
        current_row += 1
        
        # Exit Chart Configurations
        Ctk.CTkLabel(self.scrollable_frame, text="Exit Chart Type:").grid(
            row=current_row, column=0, padx=10, pady=10, sticky="w"
        )
        self.exit_chart_type_combobox = Ctk.CTkComboBox(
            self.scrollable_frame, values=["Candle Stick", "Heiken Ashi", "Renko"]
        )
        self.exit_chart_type_combobox.grid(row=current_row, column=1, padx=10, pady=10, sticky="ew")
        current_row += 1
        
        Ctk.CTkLabel(self.scrollable_frame, text="Exit Chart Timeframe:").grid(
            row=current_row, column=0, padx=10, pady=10, sticky="w"
        )
        self.exit_chart_timeframe_combobox = Ctk.CTkComboBox(
            self.scrollable_frame, values=["1m", "2m", "3M", "5M", "10M", "1H", "3H", "1D", "1W", "1M"]
        )
        self.exit_chart_timeframe_combobox.grid(row=current_row, column=1, padx=10, pady=10, sticky="ew")
        current_row += 1
        
        # ===== STOP LOSS SECTION =====
        # Create a frame for Stop Loss settings
        stop_loss_frame = Ctk.CTkFrame(self.scrollable_frame)
        stop_loss_frame.grid(row=current_row, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        stop_loss_frame.grid_columnconfigure(0, weight=1)
        stop_loss_frame.grid_columnconfigure(1, weight=1)
        
        # Stop Loss section title
        stop_loss_title = Ctk.CTkLabel(
            stop_loss_frame, 
            text="Stop Loss Settings", 
            font=("Roboto", 12, "bold")
        )
        stop_loss_title.grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 10), sticky="w")
        
        Ctk.CTkLabel(stop_loss_frame, text="Stop Loss Type:").grid(
            row=1, column=0, padx=10, pady=5, sticky="w"
        )
        self.stop_loss_type_combobox = Ctk.CTkComboBox(stop_loss_frame, values=["Price", "Percentage"])
        self.stop_loss_type_combobox.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        
        Ctk.CTkLabel(stop_loss_frame, text="Percentage Value:").grid(
            row=2, column=0, padx=10, pady=5, sticky="w"
        )
        self.stop_loss_percentage_entry = Ctk.CTkEntry(stop_loss_frame)
        self.stop_loss_percentage_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
        
        Ctk.CTkLabel(stop_loss_frame, text="Price Value:").grid(
            row=3, column=0, padx=10, pady=5, sticky="w"
        )
        self.stop_loss_price_entry = Ctk.CTkEntry(stop_loss_frame)
        self.stop_loss_price_entry.grid(row=3, column=1, padx=10, pady=5, sticky="ew")
        
        Ctk.CTkLabel(stop_loss_frame, text="Max Stop Loss per Day:").grid(
            row=4, column=0, padx=10, pady=5, sticky="w"
        )
        self.max_stop_loss_day_entry = Ctk.CTkEntry(stop_loss_frame)
        self.max_stop_loss_day_entry.grid(row=4, column=1, padx=10, pady=5, sticky="ew")
        
        Ctk.CTkLabel(stop_loss_frame, text="Max Stop Loss per Trade:").grid(
            row=5, column=0, padx=10, pady=5, sticky="w"
        )
        self.max_stop_loss_trade_entry = Ctk.CTkEntry(stop_loss_frame)
        self.max_stop_loss_trade_entry.grid(row=5, column=1, padx=10, pady=5, sticky="ew")
        
        Ctk.CTkLabel(stop_loss_frame, text="Time-Based Stop Loss (minutes):").grid(
            row=6, column=0, padx=10, pady=5, sticky="w"
        )
        self.time_based_stop_loss_entry = Ctk.CTkEntry(stop_loss_frame)
        self.time_based_stop_loss_entry.grid(row=6, column=1, padx=10, pady=5, sticky="ew")
        current_row += 1
        
        # ===== TARGET SECTION =====
        # Create a frame for Target settings
        target_frame = Ctk.CTkFrame(self.scrollable_frame)
        target_frame.grid(row=current_row, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        target_frame.grid_columnconfigure(0, weight=1)
        target_frame.grid_columnconfigure(1, weight=1)
        
        # Target (Profit) section title
        target_title = Ctk.CTkLabel(
            target_frame, 
            text="Target (Profit) Settings", 
            font=("Roboto", 12, "bold")
        )
        target_title.grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 10), sticky="w")
        
        Ctk.CTkLabel(target_frame, text="Target Type:").grid(
            row=1, column=0, padx=10, pady=5, sticky="w"
        )
        self.target_type_combobox = Ctk.CTkComboBox(target_frame, values=["Price", "Percentage"])
        self.target_type_combobox.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        
        Ctk.CTkLabel(target_frame, text="Target Percentage Value:").grid(
            row=2, column=0, padx=10, pady=5, sticky="w"
        )
        self.target_percentage_entry = Ctk.CTkEntry(target_frame)
        self.target_percentage_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
        
        Ctk.CTkLabel(target_frame, text="Target Price Value:").grid(
            row=3, column=0, padx=10, pady=5, sticky="w"
        )
        self.target_price_entry = Ctk.CTkEntry(target_frame)
        self.target_price_entry.grid(row=3, column=1, padx=10, pady=5, sticky="ew")
    
    def get_configuration(self):
        """
        Collects all the entry and exit configuration data from the form
        
        Returns:
            dict: A dictionary containing all configuration values
        """
        try:
            return {
                "entry": {
                    "chart_type": self.entry_chart_type_combobox.get(),
                    "chart_timeframe": self.entry_chart_timeframe_combobox.get(),
                    "exclude_time": {
                        "from": self.exclude_time_from_entry.get(),
                        "to": self.exclude_time_to_entry.get()
                    }
                },
                "exit": {
                    "chart_type": self.exit_chart_type_combobox.get(),
                    "chart_timeframe": self.exit_chart_timeframe_combobox.get(),
                    "stop_loss": {
                        "type": self.stop_loss_type_combobox.get(),
                        "percentage": self.stop_loss_percentage_entry.get(),
                        "price": self.stop_loss_price_entry.get(),
                        "max_per_day": self.max_stop_loss_day_entry.get(),
                        "max_per_trade": self.max_stop_loss_trade_entry.get(),
                        "time_based": self.time_based_stop_loss_entry.get()
                    },
                    "target": {
                        "type": self.target_type_combobox.get(),
                        "percentage": self.target_percentage_entry.get(),
                        "price": self.target_price_entry.get()
                    }
                }
            }
        except Exception as e:
            messagebox.showerror("Error", f"Failed to get configuration: {str(e)}")
            return {}
    
    def set_configuration(self, config):
        """
        Sets the entry and exit configuration form values from a dictionary
        
        Args:
            config (dict): A dictionary containing configuration values
        """
        try:
            if not config:
                return
                
            # Set entry configuration
            if "entry" in config:
                entry_config = config["entry"]
                if "chart_type" in entry_config:
                    self.entry_chart_type_combobox.set(entry_config["chart_type"])
                if "chart_timeframe" in entry_config:
                    self.entry_chart_timeframe_combobox.set(entry_config["chart_timeframe"])
                if "exclude_time" in entry_config:
                    exclude_time = entry_config["exclude_time"]
                    if "from" in exclude_time:
                        self.exclude_time_from_entry.delete(0, "end")
                        self.exclude_time_from_entry.insert(0, exclude_time["from"])
                    if "to" in exclude_time:
                        self.exclude_time_to_entry.delete(0, "end")
                        self.exclude_time_to_entry.insert(0, exclude_time["to"])
            
            # Set exit configuration
            if "exit" in config:
                exit_config = config["exit"]
                if "chart_type" in exit_config:
                    self.exit_chart_type_combobox.set(exit_config["chart_type"])
                if "chart_timeframe" in exit_config:
                    self.exit_chart_timeframe_combobox.set(exit_config["chart_timeframe"])
                
                # Set stop loss values
                if "stop_loss" in exit_config:
                    sl_config = exit_config["stop_loss"]
                    if "type" in sl_config:
                        self.stop_loss_type_combobox.set(sl_config["type"])
                    if "percentage" in sl_config:
                        self.stop_loss_percentage_entry.delete(0, "end")
                        self.stop_loss_percentage_entry.insert(0, sl_config["percentage"])
                    if "price" in sl_config:
                        self.stop_loss_price_entry.delete(0, "end")
                        self.stop_loss_price_entry.insert(0, sl_config["price"])
                    if "max_per_day" in sl_config:
                        self.max_stop_loss_day_entry.delete(0, "end")
                        self.max_stop_loss_day_entry.insert(0, sl_config["max_per_day"])
                    if "max_per_trade" in sl_config:
                        self.max_stop_loss_trade_entry.delete(0, "end")
                        self.max_stop_loss_trade_entry.insert(0, sl_config["max_per_trade"])
                    if "time_based" in sl_config:
                        self.time_based_stop_loss_entry.delete(0, "end")
                        self.time_based_stop_loss_entry.insert(0, sl_config["time_based"])
                
                # Set target values
                if "target" in exit_config:
                    target_config = exit_config["target"]
                    if "type" in target_config:
                        self.target_type_combobox.set(target_config["type"])
                    if "percentage" in target_config:
                        self.target_percentage_entry.delete(0, "end")
                        self.target_percentage_entry.insert(0, target_config["percentage"])
                    if "price" in target_config:
                        self.target_price_entry.delete(0, "end")
                        self.target_price_entry.insert(0, target_config["price"])
                    
        except Exception as e:
            messagebox.showerror("Error", f"Failed to set configuration: {str(e)}")