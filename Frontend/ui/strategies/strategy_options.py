import customtkinter as Ctk
# Import individual tab modules
from ui.strategies.tabs.options_config import OptionsTab
from ui.strategies.tabs.sets_config import SetTab
from ui.strategies.tabs.entry_indicators_setup import EntryIndicatorsTab
from ui.strategies.tabs.exit_indicator_setup import ExitIndicatorsTab
from ui.strategies.tabs.exit_conditions import EntryExitConfigurationsTab

class StrategyOptions(Ctk.CTkFrame):
    def __init__(self, parent, set_name=None):
        super().__init__(parent)
        # Initialize the tabview
        self.tabview = Ctk.CTkTabview(self)
        self.tabview.pack(pady=20, padx=10, fill="both", expand=True)
        
        # Add all tabs
        self.tabview.add("Set")
        self.tabview.add("Options")
        self.tabview.add("Entry Indicators")
        self.tabview.add("Exit Indicators")
        self.tabview.add("Exit/Exit Config")
        
        # Initialize each tab with its module
        self.stocks_tab = OptionsTab(self.tabview.tab("Options"))
        self.set_tab = SetTab(self.tabview.tab("Set"))
        self.entry_indicators_tab = EntryIndicatorsTab(self.tabview.tab("Entry Indicators"))
        self.exit_setup_tab = ExitIndicatorsTab(self.tabview.tab("Exit Indicators"))
        self.exit_conditions_tab = EntryExitConfigurationsTab(self.tabview.tab("Exit/Exit Config"))
        
        # Set the initial name if provided
        if set_name:
            self.set_tab.set_name_entry.insert(0, set_name)

