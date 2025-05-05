import customtkinter as Ctk

class Overview(Ctk.CTkFrame):
    def __init__(self, parent, shared_dicts):
        super().__init__(parent)
        self.shared_dicts = shared_dicts  # Store the shared dictionaries
        
        label = Ctk.CTkLabel(self, text="Overview", font=("Arial", 24, "bold"))
        label.pack(pady=20)
        
        # Rest of your code remains the same
        overview_text = """
        This is the overview section. Here you can provide a summary of the 
        application's status, key performance indicators, or any other 
        important information at a glance.

        For example, you could display:
        - Overall system health
        - Number of active connections
        - Current strategy performance
        - Recent alerts or notifications
        """

        overview_label = Ctk.CTkLabel(self, text=overview_text, wraplength=400)
        overview_label.pack(pady=10)