import customtkinter as Ctk
from.sidebar import MonitorSidebar

class MonitorView(Ctk.CTkFrame):
    def __init__(self, parent, shared_dicts):
        super().__init__(parent)
        self.shared_dicts = shared_dicts  # Store the shared dictionaries
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = MonitorSidebar(self, self.show_content)
        self.sidebar.grid(row=0, column=0, sticky="nsw", padx=10, pady=10)

        self.content_frame = Ctk.CTkFrame(self, corner_radius=15)
        self.content_frame.grid(row=0, column=1, sticky="nswe", padx=10, pady=10)
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)

        self.current_content = None
        self.show_content("stocks_set_1")  # Show the first set by default

    def show_content(self, content_name):
        if self.current_content:
            self.current_content.destroy()

        if content_name.startswith("stocks"):
            from.stocks_set import StocksSet
            self.current_content = StocksSet(self.content_frame, content_name)
        elif content_name.startswith("options"):
            from.options_set import OptionsSet
            self.current_content = OptionsSet(self.content_frame, content_name)

        self.current_content.grid(row=0, column=0, sticky="nswe", padx=10, pady=10)