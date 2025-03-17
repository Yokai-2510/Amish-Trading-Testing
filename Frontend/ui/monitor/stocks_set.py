import customtkinter as Ctk

class StocksSet(Ctk.CTkFrame):
    def __init__(self, parent, set_name):
        super().__init__(parent)

        # Tabview
        self.tabview = Ctk.CTkTabview(self)
        self.tabview.pack(pady=20, padx=10, fill="both", expand=True)
        self.tabview.add("Market Data")  # Changed tab name
        self.tabview.add("Indicators")   # Changed tab name
        self.tabview.add("Trades")        # Changed tab name

        # Add content to each tab
        Ctk.CTkLabel(self.tabview.tab("Market Data"), text=f"Stocks - {set_name} - Market Data").pack()
        Ctk.CTkLabel(self.tabview.tab("Indicators"), text=f"Stocks - {set_name} - Indicators").pack()
        Ctk.CTkLabel(self.tabview.tab("Trades"), text=f"Stocks - {set_name} - Trades").pack()