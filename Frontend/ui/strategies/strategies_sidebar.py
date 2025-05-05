import customtkinter as Ctk

class StrategiesSidebar(Ctk.CTkFrame):
    def __init__(self, parent, show_content_callback):
        super().__init__(parent, width=220, corner_radius=15)
        self.grid_rowconfigure(10, weight=1)  # Adjust weight as needed
        self.show_content = show_content_callback

        Ctk.CTkLabel(self, text="Strategies Menu", font=("Arial", 20, "bold")).pack(pady=(20, 10))

        # Stocks Section
        Ctk.CTkLabel(self, text="Stocks", font=("Arial", 16)).pack(pady=(10, 5))
        for i in range(1, 5):
            btn = Ctk.CTkButton(self, text=f"Set {i}", command=lambda name=f"stocks_set_{i}": self.show_content(name), width=180, corner_radius=10)
            btn.pack(pady=5, padx=10)  # Add padding for margin

        # Options Section
        Ctk.CTkLabel(self, text="Options", font=("Arial", 16)).pack(pady=(10, 5))
        for i in range(1, 9):
            btn = Ctk.CTkButton(self, text=f"Set {i}", command=lambda name=f"options_set_{i}": self.show_content(name), width=180, corner_radius=10)
            btn.pack(pady=5, padx=10)  # Add padding for margin