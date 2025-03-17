# ui/app.py
import customtkinter as Ctk
from ui.sidebar import Sidebar
from ui.overview.overview import Overview
from ui.configure.configure import Configure
from ui.connect.connect_view import Connect
from ui.monitor.monitor_view import MonitorView
from ui.strategies.strategies_view import StrategiesView

class App(Ctk.CTk):
    def __init__(self, shared_dicts):
        super().__init__()
        self.shared_dicts = shared_dicts  # Store dicts here

        self.title("Amish Trading Bot")
        self.geometry("1366x768")
        self.minsize(600, 480)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = Sidebar(self, self.show_content)
        self.sidebar.grid(row=0, column=0, sticky="nsw", padx=10, pady=10)
        self.content_frame = Ctk.CTkFrame(self, corner_radius=15)
        self.content_frame.grid(row=0, column=1, sticky="nswe", padx=10, pady=10)
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)

        self.current_content = None
        self.show_content("overview")

    def show_content(self, content_name):
        if self.current_content:
            self.current_content.destroy()

        if content_name == "overview":
            self.current_content = Overview(self.content_frame, self.shared_dicts)
        elif content_name == "configure":
            self.current_content = Configure(self.content_frame, self.shared_dicts)
        elif content_name == "connect":
            self.current_content = Connect(self.content_frame, self.shared_dicts)
        elif content_name == "monitor":
            self.current_content = MonitorView(self.content_frame, self.shared_dicts)
        elif content_name == "strategies":
            self.current_content = StrategiesView(self.content_frame, self.shared_dicts)

        self.current_content.grid(row=0, column=0, sticky="nswe", padx=10, pady=10)