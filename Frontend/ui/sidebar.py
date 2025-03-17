import customtkinter as Ctk

class Sidebar(Ctk.CTkFrame):
    def __init__(self, parent, show_content_callback):
        super().__init__(parent, width=220, corner_radius=15)
        self.grid_rowconfigure(6, weight=1)  # Adjust weight as needed
        self.show_content = show_content_callback

        self.logo_label = Ctk.CTkLabel(self, text="Menu", font=("Arial", 22, "bold"))
        self.logo_label.pack(pady=(20, 20))

        self.buttons = [
            ("Overview", "overview"),
            ("Configure", "configure"),
            ("Connect", "connect"),
            ("Monitor", "monitor"),
            ("Strategies", "strategies")
        ]

        for text, content_name in self.buttons:
            btn = Ctk.CTkButton(self, text=text, command=lambda name=content_name: self.show_content(name), width=180, corner_radius=10)
            btn.pack(pady=10, padx=15)  

        # Logout Button
        self.logout_button = Ctk.CTkButton(self, text="🚪 Logout", command=parent.destroy, width=180, corner_radius=10)
        self.logout_button.pack(pady=10, padx=10)