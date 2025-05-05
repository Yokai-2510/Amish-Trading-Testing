import customtkinter as Ctk
from tkinter import messagebox

class StocksTab:
    def __init__(self, parent):
        self.parent = parent
        self.parent.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        # Store selected stocks with their quantities
        self.stocks = []
        
        # Sample stock collections (these would be populated from your data source)
        self.stock_collections = {
            "NIFTY50": ["RELIANCE", "TCS", "HDFC", "INFY", "ICICI", "HUL", "ITC", "SBI", "BHARTIARTL", "KOTAKBANK"],
            "BANK NIFTY": ["HDFCBANK", "ICICIBANK", "SBIN", "KOTAKBANK", "AXISBANK", "INDUSINDBK", "BANKBARODA", "FEDERALBNK", "PNB", "IDFCFIRSTB"],
            "IT": ["TCS", "INFY", "WIPRO", "HCLTECH", "TECHM", "LTIM", "MPHASIS", "PERSISTENT", "COFORGE", "OFSS"],
            "PHARMA": ["SUNPHARMA", "DRREDDY", "CIPLA", "DIVISLAB", "BIOCON", "AUROPHARMA", "LUPIN", "ALKEM", "TORNTPHARM", "GLAXO"]
        }
        
        # Available individual stocks (this would be a larger list in your actual implementation)
        self.available_stocks = []
        for stocks in self.stock_collections.values():
            self.available_stocks.extend(stocks)
        self.available_stocks = sorted(list(set(self.available_stocks)))
        
        # Create all widgets
        self._create_widgets()
        
    def _create_widgets(self):
        # Top control panel - row 0
        control_panel = Ctk.CTkFrame(self.parent)
        control_panel.grid(row=0, column=0, columnspan=4, padx=10, pady=5, sticky="ew")
        control_panel.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)
        
        # Title and default quantity in the same row
        Ctk.CTkLabel(
            control_panel, 
            text="Stocks Configuration", 
            font=("Helvetica", 16, "bold")
        ).grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky="w")
        
        Ctk.CTkLabel(control_panel, text="Default Qty:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.default_quantity_entry = Ctk.CTkEntry(control_panel, width=60)
        self.default_quantity_entry.grid(row=0, column=3, padx=5, pady=5, sticky="w")
        self.default_quantity_entry.insert(0, "1")
        
        self.apply_default_btn = Ctk.CTkButton(
            control_panel,
            text="Apply to All",
            command=self.apply_default_quantity,
            width=100,
            height=28
        )
        self.apply_default_btn.grid(row=0, column=4, padx=5, pady=5, sticky="w")
        
        self.clear_all_btn = Ctk.CTkButton(
            control_panel,
            text="Clear All",
            fg_color="firebrick3",
            hover_color="firebrick4",
            command=self.clear_all_stocks,
            width=80,
            height=28
        )
        self.clear_all_btn.grid(row=0, column=5, padx=5, pady=5, sticky="e")
        
        # Add Stock controls - row 1
        add_panel = Ctk.CTkFrame(self.parent)
        add_panel.grid(row=1, column=0, columnspan=4, padx=10, pady=5, sticky="ew")
        add_panel.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)
        
        # Individual stock selection - left side
        Ctk.CTkLabel(add_panel, text="Stock:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.stock_combobox = Ctk.CTkComboBox(
            add_panel, 
            values=self.available_stocks,
            width=120
        )
        if self.available_stocks:
            self.stock_combobox.set(self.available_stocks[0])
        self.stock_combobox.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        Ctk.CTkLabel(add_panel, text="Qty:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.quantity_entry = Ctk.CTkEntry(add_panel, width=50)
        self.quantity_entry.grid(row=0, column=3, padx=5, pady=5, sticky="w")
        self.quantity_entry.insert(0, "1")
        
        self.add_button = Ctk.CTkButton(
            add_panel, 
            text="Add Stock", 
            command=self.add_stock,
            width=90,
            height=28
        )
        self.add_button.grid(row=0, column=4, padx=5, pady=5, sticky="w")
        
        # Collection selection - right side
        Ctk.CTkLabel(add_panel, text="Collection:").grid(row=0, column=5, padx=5, pady=5, sticky="e")
        self.collection_combobox = Ctk.CTkComboBox(
            add_panel, 
            values=list(self.stock_collections.keys()),
            width=120
        )
        if self.stock_collections:
            self.collection_combobox.set(list(self.stock_collections.keys())[0])
        self.collection_combobox.grid(row=0, column=6, padx=5, pady=5, sticky="w")
        
        self.add_collection_button = Ctk.CTkButton(
            add_panel, 
            text="Add Collection", 
            command=self.add_collection,
            width=110,
            height=28
        )
        self.add_collection_button.grid(row=0, column=7, padx=5, pady=5, sticky="w")
        
        # Selected Stocks section - row 2 (header)
        header_frame = Ctk.CTkFrame(self.parent)
        header_frame.grid(row=2, column=0, columnspan=4, padx=10, pady=(5, 0), sticky="ew")
        header_frame.grid_columnconfigure((0, 1), weight=1)
        
        Ctk.CTkLabel(
            header_frame, 
            text="Selected Trading Instruments", 
            font=("Helvetica", 14, "bold")
        ).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        self.count_label = Ctk.CTkLabel(
            header_frame, 
            text="Selected Stocks: 0/30"
        )
        self.count_label.grid(row=0, column=1, padx=5, pady=5, sticky="e")
        
        # Scrollable list frame - row 3 (give it most of the space)
        self.list_container = Ctk.CTkFrame(self.parent)
        self.list_container.grid(row=3, column=0, columnspan=4, padx=10, pady=5, sticky="nsew")
        self.parent.grid_rowconfigure(3, weight=10)  # Give this row most of the weight
        
        # Create a scrollable frame for stocks list
        self.scrollable_frame = Ctk.CTkScrollableFrame(self.list_container)
        self.scrollable_frame.pack(fill="both", expand=True)
        
        # Configure columns for the scrollable frame
        self.scrollable_frame.grid_columnconfigure(0, weight=2)  # Stock name
        self.scrollable_frame.grid_columnconfigure(1, weight=1)  # Quantity
        self.scrollable_frame.grid_columnconfigure(2, weight=1)  # Action
        
        # Headers for stocks list
        Ctk.CTkLabel(self.scrollable_frame, text="Stock", font=("Helvetica", 12, "bold")).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        Ctk.CTkLabel(self.scrollable_frame, text="Quantity", font=("Helvetica", 12, "bold")).grid(row=0, column=1, padx=10, pady=5, sticky="w")
        Ctk.CTkLabel(self.scrollable_frame, text="Action", font=("Helvetica", 12, "bold")).grid(row=0, column=2, padx=10, pady=5, sticky="w")
        
        # Separator in scrollable frame
        separator = Ctk.CTkFrame(self.scrollable_frame, height=2, fg_color="gray")
        separator.grid(row=1, column=0, columnspan=3, sticky="ew", padx=5, pady=5)
        
        # Initial empty list message
        self.update_stocks_list()
    
    def add_stock(self):
        """Add a single stock to the list"""
        stock_name = self.stock_combobox.get()
        quantity = self.quantity_entry.get()
        
        # Validate inputs
        if not stock_name:
            messagebox.showerror("Error", "Please select a stock")
            return
        
        try:
            quantity = int(quantity)
            if quantity <= 0:
                raise ValueError("Quantity must be positive")
        except ValueError:
            messagebox.showerror("Error", "Quantity must be a positive integer")
            return
        
        # Check if stock is already added
        if any(s["name"] == stock_name for s in self.stocks):
            messagebox.showerror("Error", f"{stock_name} is already in the list")
            return
        
        # Check maximum stocks limit
        if len(self.stocks) >= 30:
            messagebox.showerror("Error", "Maximum limit of 30 stocks reached")
            return
        
        # Add to stocks list
        self.stocks.append({
            "name": stock_name,
            "quantity": quantity
        })
        
        # Update the display
        self.update_stocks_list()
        
        # Clear entry field
        self.quantity_entry.delete(0, Ctk.END)
        self.quantity_entry.insert(0, self.default_quantity_entry.get())
    
    def add_collection(self):
        """Add a collection of stocks to the list"""
        collection_name = self.collection_combobox.get()
        
        if not collection_name or collection_name not in self.stock_collections:
            messagebox.showerror("Error", "Please select a valid collection")
            return
        
        # Get stocks from the selected collection
        collection_stocks = self.stock_collections[collection_name]
        quantity = int(self.default_quantity_entry.get())
        
        # Check maximum stocks limit
        if len(self.stocks) + len(collection_stocks) > 30:
            messagebox.showerror("Error", f"Adding {len(collection_stocks)} stocks would exceed the limit of 30")
            return
        
        # Add each stock from the collection
        for stock in collection_stocks:
            # Skip if already in the list
            if any(s["name"] == stock for s in self.stocks):
                continue
                
            self.stocks.append({
                "name": stock,
                "quantity": quantity
            })
        
        # Update the display
        self.update_stocks_list()
    
    def remove_stock(self, stock_name):
        """Remove a stock from the list"""
        self.stocks = [s for s in self.stocks if s["name"] != stock_name]
        self.update_stocks_list()
    
    def clear_all_stocks(self):
        """Clear all stocks from the list"""
        if messagebox.askyesno("Confirm", "Are you sure you want to clear all stocks?"):
            self.stocks = []
            self.update_stocks_list()
    
    def apply_default_quantity(self):
        """Apply the default quantity to all stocks"""
        try:
            quantity = int(self.default_quantity_entry.get())
            if quantity <= 0:
                raise ValueError("Quantity must be positive")
                
            for stock in self.stocks:
                stock["quantity"] = quantity
                
            self.update_stocks_list()
            
        except ValueError:
            messagebox.showerror("Error", "Default quantity must be a positive integer")
    
    def update_stocks_list(self):
        """Update the displayed list of stocks"""
        # Clear existing items (except headers and separator)
        for widget in self.scrollable_frame.grid_slaves():
            if int(widget.grid_info()["row"]) > 1:
                widget.destroy()
        
        if not self.stocks:
            # Show empty message
            empty_label = Ctk.CTkLabel(self.scrollable_frame, text="No stocks added yet")
            empty_label.grid(row=2, column=0, columnspan=3, padx=10, pady=20)
        else:
            # Add each stock to the display
            for i, stock in enumerate(self.stocks):
                row = i + 2  # Start after header and separator
                
                # Stock name
                Ctk.CTkLabel(self.scrollable_frame, text=stock["name"]).grid(
                    row=row, column=0, padx=10, pady=3, sticky="w"
                )
                
                # Quantity with editable entry
                qty_entry = Ctk.CTkEntry(self.scrollable_frame, width=60)
                qty_entry.grid(row=row, column=1, padx=10, pady=3)
                qty_entry.insert(0, str(stock["quantity"]))
                
                # Save quantity on focus out
                qty_entry.bind("<FocusOut>", lambda e, name=stock["name"], entry=qty_entry: 
                               self.update_stock_quantity(name, entry.get()))
                # Also save on Enter key
                qty_entry.bind("<Return>", lambda e, name=stock["name"], entry=qty_entry: 
                               self.update_stock_quantity(name, entry.get()))
                
                # Remove button
                remove_btn = Ctk.CTkButton(
                    self.scrollable_frame,
                    text="Remove",
                    fg_color="firebrick3",
                    hover_color="firebrick4",
                    width=70,
                    height=24,
                    command=lambda name=stock["name"]: self.remove_stock(name)
                )
                remove_btn.grid(row=row, column=2, padx=10, pady=3)
        
        # Update stocks counter
        self.count_label.configure(text=f"Selected Stocks: {len(self.stocks)}/30")
    
    def update_stock_quantity(self, stock_name, quantity):
        """Update the quantity of a specific stock"""
        try:
            quantity = int(quantity)
            if quantity <= 0:
                raise ValueError()
                
            for stock in self.stocks:
                if stock["name"] == stock_name:
                    stock["quantity"] = quantity
                    break
                    
        except ValueError:
            messagebox.showerror("Error", "Quantity must be a positive integer")
            self.update_stocks_list()  # Refresh with correct values
    
    def get_config(self):
        """Get all stocks configuration as a dictionary"""
        return {
            "default_quantity": self.default_quantity_entry.get(),
            "stocks": self.stocks
        }
    
    def set_config(self, config_dict):
        """Set values from a dictionary"""
        if "default_quantity" in config_dict:
            self.default_quantity_entry.delete(0, Ctk.END)
            self.default_quantity_entry.insert(0, config_dict["default_quantity"])
            
        if "stocks" in config_dict:
            self.stocks = config_dict["stocks"]
            self.update_stocks_list()