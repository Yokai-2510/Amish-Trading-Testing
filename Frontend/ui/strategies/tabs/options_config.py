import customtkinter as Ctk
from datetime import datetime, timedelta
import calendar

class OptionsTab:
    def __init__(self, parent):
        self.parent = parent
        self.parent.grid_columnconfigure((0, 1), weight=1)
        
        # Define expiry rules for each index
        self.expiry_rules = {
            "NIFTY": {"day": 3, "weekly": True},       # Thursday expirations
            "BANKNIFTY": {"day": 3, "weekly": True},   # Thursday expirations
            "FINNIFTY": {"day": 1, "weekly": True},    # Tuesday expirations
            "MIDCPNIFTY": {"day": 2, "weekly": True},  # Wednesday expirations
            "SENSEX": {"day": 3, "weekly": True}       # Thursday expirations
        }
        
        # Create all widgets
        self._create_widgets()
        
        # Setup expiry dates based on default index
        self._update_expiry_dates()
        
    def _create_widgets(self):
        # Index Selector at the top
        Ctk.CTkLabel(self.parent, text="Options Index:").grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.index_combobox = Ctk.CTkComboBox(self.parent, values=["NIFTY", "BANKNIFTY", "FINNIFTY", "MIDCPNIFTY", "SENSEX"], 
                                              command=self._update_expiry_dates)
        self.index_combobox.grid(row=0, column=1, padx=150, pady=10, sticky="ew")
        
        # Option Type
        Ctk.CTkLabel(self.parent, text="Option Type:").grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        self.option_type_combobox = Ctk.CTkComboBox(self.parent, values=["CE", "PE"])
        self.option_type_combobox.grid(row=1, column=1, padx=150, pady=10, sticky="ew")
        
        # Option Buying or Selling
        Ctk.CTkLabel(self.parent, text="Trade Type:").grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        self.buy_sell_combobox = Ctk.CTkComboBox(self.parent, values=["Buy", "Sell"])
        self.buy_sell_combobox.grid(row=2, column=1, padx=150, pady=10, sticky="ew")
        
        # Strike Selection
        Ctk.CTkLabel(self.parent, text="Strike Selection:").grid(row=3, column=0, padx=10, pady=10, sticky="ew")
        self.strike_selection_combobox = Ctk.CTkComboBox(self.parent, values=["ATM", "OTM", "ITM"])
        self.strike_selection_combobox.grid(row=3, column=1, padx=150, pady=10, sticky="ew")
        
        # OTM/ITM Strike Selection
        Ctk.CTkLabel(self.parent, text="OTM/ITM Strike:").grid(row=4, column=0, padx=10, pady=10, sticky="ew")
        self.otm_itm_strike_entry = Ctk.CTkEntry(self.parent)
        self.otm_itm_strike_entry.grid(row=4, column=1, padx=100, pady=10, sticky="ew")
        
        # Lot Size
        Ctk.CTkLabel(self.parent, text="Lot Size:").grid(row=5, column=0, padx=10, pady=10, sticky="ew")
        self.lot_size_entry = Ctk.CTkEntry(self.parent)
        self.lot_size_entry.grid(row=5, column=1, padx=100, pady=10, sticky="ew")
        
        # Expiry Selection - Use ComboBox instead of Entry for selecting from a list
        Ctk.CTkLabel(self.parent, text="Expiry:").grid(row=7, column=0, padx=10, pady=10, sticky="ew")
        self.expiry_combobox = Ctk.CTkComboBox(self.parent, values=[])
        self.expiry_combobox.grid(row=7, column=1, padx=150, pady=10, sticky="ew")
        
        # Set default values
        self.index_combobox.set("NIFTY")
        self.option_type_combobox.set("CE")
        self.buy_sell_combobox.set("Buy")
        self.strike_selection_combobox.set("ATM")
        
    def _update_expiry_dates(self, *args):
        """Update the expiry dates based on the selected index"""
        selected_index = self.index_combobox.get()
        expiry_dates = self._get_next_expiry_dates(selected_index, 8)  # Get next 8 expiry dates
        
        # Format dates for display
        formatted_dates = [f"{date.strftime('%d-%b-%Y')} ({self._get_day_name(date)})" for date in expiry_dates]
        
        # Update the combobox with new values
        self.expiry_combobox.configure(values=formatted_dates)
        
        # Set the first expiry date as default
        if formatted_dates:
            self.expiry_combobox.set(formatted_dates[0])
    
    def _get_next_expiry_dates(self, index, count=8):
        """Get the next 'count' expiry dates for the given index"""
        today = datetime.now().date()
        
        # Get the weekday for expiry (0=Monday, 1=Tuesday, ..., 6=Sunday)
        target_weekday = self.expiry_rules[index]["day"]
        
        expiry_dates = []
        current_date = today
        
        # Find the first upcoming expiry
        days_ahead = (target_weekday - today.weekday()) % 7
        if days_ahead == 0 and datetime.now().hour >= 15:  # If today is expiry day but after market hours
            days_ahead = 7
        
        first_expiry = today + timedelta(days=days_ahead)
        current_date = first_expiry
        
        # Add subsequent expiry dates
        for _ in range(count):
            expiry_dates.append(current_date)
            # Add 7 days for weekly expiry
            if self.expiry_rules[index]["weekly"]:
                current_date = current_date + timedelta(days=7)
            else:
                # For monthly expiry logic (last Thursday of month)
                # This is a simplified version - adjust as needed
                current_date = self._get_next_monthly_expiry(current_date, target_weekday)
        
        return expiry_dates
    
    def _get_next_monthly_expiry(self, current_date, target_weekday):
        """Get the next monthly expiry date (usually last Thursday of the month)"""
        # Move to the next month
        if current_date.month == 12:
            next_month = 1
            next_year = current_date.year + 1
        else:
            next_month = current_date.month + 1
            next_year = current_date.year
            
        # Get the last day of the next month
        last_day = calendar.monthrange(next_year, next_month)[1]
        last_date = datetime(next_year, next_month, last_day).date()
        
        # Find the last target weekday of the month
        offset = (last_date.weekday() - target_weekday) % 7
        last_target_date = last_date - timedelta(days=offset)
        
        # If the last target date is the last day of the month, go to previous occurrence
        if offset == 0:
            last_target_date = last_target_date - timedelta(days=7)
            
        return last_target_date
    
    def _get_day_name(self, date):
        """Return the day name for a date"""
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        return days[date.weekday()]
    
    def get_config(self):
        """Get all values from the options tab as a dictionary"""
        # Extract just the date portion from the expiry string
        expiry_full = self.expiry_combobox.get()
        expiry_date = expiry_full.split(" ")[0] if expiry_full else ""
        
        return {
            "index": self.index_combobox.get(),
            "option_type": self.option_type_combobox.get(),
            "trade_type": self.buy_sell_combobox.get(),
            "strike_selection": self.strike_selection_combobox.get(),
            "otm_itm_strike": self.otm_itm_strike_entry.get(),
            "lot_size": self.lot_size_entry.get(),
            "expiry": expiry_date,
            "expiry_full": expiry_full
        }
    
    def set_config(self, config_dict):
        """Set values from a dictionary to all widgets"""
        if "index" in config_dict:
            self.index_combobox.set(config_dict["index"])
            # Update expiry dates when index changes
            self._update_expiry_dates()
            
        if "option_type" in config_dict:
            self.option_type_combobox.set(config_dict["option_type"])
        if "trade_type" in config_dict:
            self.buy_sell_combobox.set(config_dict["trade_type"])
        if "strike_selection" in config_dict:
            self.strike_selection_combobox.set(config_dict["strike_selection"])
        if "otm_itm_strike" in config_dict:
            self.otm_itm_strike_entry.delete(0, "end")
            self.otm_itm_strike_entry.insert(0, config_dict["otm_itm_strike"])
        if "lot_size" in config_dict:
            self.lot_size_entry.delete(0, "end")
            self.lot_size_entry.insert(0, config_dict["lot_size"])
        if "expiry_full" in config_dict and config_dict["expiry_full"] in self.expiry_combobox._values:
            self.expiry_combobox.set(config_dict["expiry_full"])
        elif "expiry" in config_dict:
            # Try to find matching date format in available options
            for option in self.expiry_combobox._values:
                if option.startswith(config_dict["expiry"]):
                    self.expiry_combobox.set(option)
                    break