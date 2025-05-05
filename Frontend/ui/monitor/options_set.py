import customtkinter as Ctk

class OptionsSet(Ctk.CTkFrame):
    def __init__(self, parent, set_name):
        super().__init__(parent)

        # Tabview
        self.tabview = Ctk.CTkTabview(self)
        self.tabview.pack(pady=20, padx=10, fill="both", expand=True)
        self.tabview.add("Options Data")  # Changed tab name
        self.tabview.add("Trades")        # Changed tab name
        self.tabview.add("PnL")           # Changed tab name

        # Add content to each tab
        Ctk.CTkLabel(self.tabview.tab("Options Data"), text=f"Options - {set_name} - Options Data").pack()
        Ctk.CTkLabel(self.tabview.tab("Trades"), text=f"Options - {set_name} - Trades").pack()
        Ctk.CTkLabel(self.tabview.tab("PnL"), text=f"Options - {set_name} - PnL").pack()