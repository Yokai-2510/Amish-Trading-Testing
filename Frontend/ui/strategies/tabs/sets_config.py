import customtkinter as Ctk

# Add Chart type and Chart Time frame here 

class SetTab:
    def __init__(self, parent):
        self.parent = parent
        self.parent.grid_columnconfigure((0, 1), weight=1)
        
        # Set Name
        Ctk.CTkLabel(self.parent, text="Set Name:").grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.set_name_entry = Ctk.CTkEntry(self.parent)
        self.set_name_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        # Set Active Status
        Ctk.CTkLabel(self.parent, text="Active:").grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        self.active_switch = Ctk.CTkSwitch(self.parent)
        self.active_switch.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        
        # Broker Selection
        Ctk.CTkLabel(self.parent, text="Broker:").grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        self.broker_combobox = Ctk.CTkComboBox(self.parent, values=["Kotak", "UPSTOX" , "FYERS" , "ZERODHA"])
        self.broker_combobox.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
        
        # Start Time
        Ctk.CTkLabel(self.parent, text="Start Time:").grid(row=3, column=0, padx=10, pady=10, sticky="ew")
        self.start_time_entry = Ctk.CTkEntry(self.parent)
        self.start_time_entry.grid(row=3, column=1, padx=10, pady=10, sticky="ew")
        
        # End Time
        Ctk.CTkLabel(self.parent, text="End Time:").grid(row=4, column=0, padx=10, pady=10, sticky="ew")
        self.end_time_entry = Ctk.CTkEntry(self.parent)
        self.end_time_entry.grid(row=4, column=1, padx=10, pady=10, sticky="ew")
        
        # Entry conditions Check interval
        Ctk.CTkLabel(self.parent, text="Entry Check Interval (s):").grid(row=5, column=0, padx=10, pady=10, sticky="ew")
        self.entry_interval_entry = Ctk.CTkEntry(self.parent)
        self.entry_interval_entry.grid(row=5, column=1, padx=10, pady=10, sticky="ew")
        
        # Exit conditions check interval
        Ctk.CTkLabel(self.parent, text="Exit Check Interval (s):").grid(row=6, column=0, padx=10, pady=10, sticky="ew")
        self.exit_interval_entry = Ctk.CTkEntry(self.parent)
        self.exit_interval_entry.grid(row=6, column=1, padx=10, pady=10, sticky="ew")