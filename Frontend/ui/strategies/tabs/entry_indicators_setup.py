import customtkinter as Ctk
from tkinter import messagebox
from ui.strategies.tabs.entry_indicator_config import IndicatorConfigDialog

class EntryIndicatorsTab:
    def __init__(self, parent):
        self.parent = parent
        self.parent.grid_columnconfigure((0, 1, 2), weight=1)
        
        # Store indicators list with their logic operators and parameters
        self.indicators = []
        self.current_sequence = 0
        
        # Available indicators list from your specifications
        self.available_indicators = [
            "Bollinger Bands", "RSI", "Stochastic RSI", "Moving Averages",
            "MACD", "ADX", "Volume", "Super-trend", "Fibonacci", "Up Trend", "Down Trend"
        ]
        
        # Create all widgets
        self._create_widgets()
        
    def _create_widgets(self):
        # Title Label
        title_label = Ctk.CTkLabel(
            self.parent, 
            text="Entry Setup Configuration", 
            font=("Helvetica", 16, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=3, padx=20, pady=(20, 10), sticky="ew")
        
        # Frame for adding new indicators
        self.add_frame = Ctk.CTkFrame(self.parent)
        self.add_frame.grid(row=1, column=0, columnspan=3, padx=20, pady=10, sticky="ew")
        self.add_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        # Indicator Selection
        Ctk.CTkLabel(self.add_frame, text="Indicator:").grid(row=0, column=0, padx=10, pady=10)
        self.indicator_combobox = Ctk.CTkComboBox(
            self.add_frame, 
            values=self.available_indicators
        )
        self.indicator_combobox.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        self.indicator_combobox.set(self.available_indicators[0])
        
        # Logic Operator Selection
        Ctk.CTkLabel(self.add_frame, text="Logic:").grid(row=1, column=0, padx=10, pady=10)
        self.logic_combobox = Ctk.CTkComboBox(
            self.add_frame, 
            values=["AND", "OR"]
        )
        self.logic_combobox.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        self.logic_combobox.set("AND")
        
        # Add Button
        self.add_button = Ctk.CTkButton(
            self.add_frame, 
            text="Add Indicator", 
            command=self.add_indicator
        )
        self.add_button.grid(row=2, column=0, columnspan=3, padx=20, pady=20, sticky="ew")
        
        # Create a frame for the bulk actions
        self.bulk_action_frame = Ctk.CTkFrame(self.parent)
        self.bulk_action_frame.grid(row=2, column=0, columnspan=3, padx=20, pady=(10, 10), sticky="ew")
        self.bulk_action_frame.grid_columnconfigure((0, 1), weight=1)
        
        # Add Activate All button
        self.activate_all_button = Ctk.CTkButton(
            self.bulk_action_frame,
            text="Activate All Indicators",
            command=self.activate_all_indicators
        )
        self.activate_all_button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        # Add Deactivate All button
        self.deactivate_all_button = Ctk.CTkButton(
            self.bulk_action_frame,
            text="Deactivate All Indicators",
            command=self.deactivate_all_indicators
        )
        self.deactivate_all_button.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        # Create a container frame for the scrollable frame
        self.list_container = Ctk.CTkFrame(self.parent)
        self.list_container.grid(row=3, column=0, columnspan=3, padx=20, pady=(10, 10), sticky="nsew")
        self.list_container.grid_columnconfigure(0, weight=1)
        self.list_container.grid_rowconfigure(0, weight=1)
        
        # Create the scrollable frame for displaying added indicators
        self.scrollable_frame = Ctk.CTkScrollableFrame(self.list_container)
        self.scrollable_frame.grid(row=0, column=0, sticky="nsew")
        self.scrollable_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)
        
        # Headers
        Ctk.CTkLabel(self.scrollable_frame, text="Sequence", font=("Helvetica", 12, "bold")).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        Ctk.CTkLabel(self.scrollable_frame, text="Indicator", font=("Helvetica", 12, "bold")).grid(row=0, column=1, padx=10, pady=5, sticky="w")
        Ctk.CTkLabel(self.scrollable_frame, text="Logic", font=("Helvetica", 12, "bold")).grid(row=0, column=2, padx=10, pady=5, sticky="w")
        Ctk.CTkLabel(self.scrollable_frame, text="Status", font=("Helvetica", 12, "bold")).grid(row=0, column=3, padx=10, pady=5, sticky="w")
        Ctk.CTkLabel(self.scrollable_frame, text="Action", font=("Helvetica", 12, "bold")).grid(row=0, column=4, padx=10, pady=5, sticky="w")
        
        # Create a separator
        separator = Ctk.CTkFrame(self.scrollable_frame, height=2, fg_color="gray")
        separator.grid(row=1, column=0, columnspan=5, sticky="ew", padx=5, pady=5)
        
        # Empty indicator list message
        self.empty_label = Ctk.CTkLabel(self.scrollable_frame, text="No indicators added yet")
        self.empty_label.grid(row=2, column=0, columnspan=5, padx=10, pady=20)
    
    def add_indicator(self):
        """Add a new indicator to the list with its logic operator and parameters"""
        indicator_type = self.indicator_combobox.get()
        logic_operator = self.logic_combobox.get()
        
        # Configure the indicator using a dialog
        config_dialog = IndicatorConfigDialog(self.parent, indicator_type)
        
        # If user canceled, exit early
        if not config_dialog.result:
            return
        
        # First indicator doesn't need a logic operator
        if len(self.indicators) == 0:
            logic_operator = "FIRST"
        
        # Add to indicators list with active status (default is active)
        self.current_sequence += 1
        self.indicators.append({
            "sequence": self.current_sequence,
            "indicator_type": indicator_type,
            "indicator_name": config_dialog.result["display_name"],
            "parameters": config_dialog.result["parameters"],
            "logic": logic_operator,
            "active": True  # Default to active
        })
        
        # Update the display
        self.update_indicator_list()
    
    def remove_indicator(self, sequence):
        """Remove an indicator from the list"""
        # Find and remove the indicator with the given sequence number
        self.indicators = [ind for ind in self.indicators if ind["sequence"] != sequence]
        
        # Resequence the indicators to keep continuous numbering
        self.resequence_indicators()
        
        # Update display
        self.update_indicator_list()
    
    def resequence_indicators(self):
        """Update sequence numbers after removal to be continuous"""
        for i, indicator in enumerate(self.indicators):
            indicator["sequence"] = i + 1
        
        # Update the current sequence counter
        if self.indicators:
            self.current_sequence = max(ind["sequence"] for ind in self.indicators)
        else:
            self.current_sequence = 0
    
    def edit_indicator(self, sequence):
        """Edit an existing indicator's parameters"""
        # Find the indicator with the given sequence
        indicator = next((ind for ind in self.indicators if ind["sequence"] == sequence), None)
        if not indicator:
            return
        
        # Create a configuration dialog for the indicator type
        config_dialog = IndicatorConfigDialog(self.parent, indicator["indicator_type"])
        
        # Pre-fill the dialog with existing values
        for param_name, param_value in indicator["parameters"].items():
            if param_name in config_dialog.param_entries:
                entry = config_dialog.param_entries[param_name]
                entry.delete(0, 'end')
                entry.insert(0, str(param_value))
        
        config_dialog.display_name.delete(0, 'end')
        config_dialog.display_name.insert(0, indicator["indicator_name"])
        
        # If user canceled, exit early
        if not config_dialog.result:
            return
        
        # Update the indicator
        indicator["indicator_name"] = config_dialog.result["display_name"]
        indicator["parameters"] = config_dialog.result["parameters"]
        
        # Update display
        self.update_indicator_list()
    
    def toggle_indicator_status(self, sequence):
        """Toggle active status of an indicator"""
        # Find the indicator with the given sequence
        indicator = next((ind for ind in self.indicators if ind["sequence"] == sequence), None)
        if indicator:
            # Toggle the active status
            indicator["active"] = not indicator["active"]
            # Update display
            self.update_indicator_list()
    
    def activate_all_indicators(self):
        """Set all indicators to active"""
        for indicator in self.indicators:
            indicator["active"] = True
        self.update_indicator_list()
    
    def deactivate_all_indicators(self):
        """Set all indicators to inactive"""
        for indicator in self.indicators:
            indicator["active"] = False
        self.update_indicator_list()
    
    def update_indicator_list(self):
        """Update the displayed list of indicators"""
        # Clear existing items
        for widget in self.scrollable_frame.grid_slaves():
            if int(widget.grid_info()["row"]) > 1:  # Keep the header and separator
                widget.destroy()
        
        if not self.indicators:
            # Show empty message
            self.empty_label = Ctk.CTkLabel(self.scrollable_frame, text="No indicators added yet")
            self.empty_label.grid(row=2, column=0, columnspan=5, padx=10, pady=20)
            return
        
        # Add each indicator to the display
        for i, indicator in enumerate(self.indicators):
            row = i + 2  # Start after header and separator
            
            # Sequence number
            Ctk.CTkLabel(self.scrollable_frame, text=str(indicator["sequence"])).grid(row=row, column=0, padx=10, pady=5, sticky="w")
            
            # Indicator name only (without parameters)
            Ctk.CTkLabel(self.scrollable_frame, text=indicator["indicator_name"]).grid(row=row, column=1, padx=10, pady=5, sticky="w")
            
            # Logic operator
            logic_text = indicator["logic"]
            Ctk.CTkLabel(self.scrollable_frame, text=logic_text).grid(row=row, column=2, padx=10, pady=5, sticky="w")
            
            # Status indicator
            status_text = "ON" if indicator["active"] else "OFF"
            status_color = "green" if indicator["active"] else "red"
            status_label = Ctk.CTkLabel(
                self.scrollable_frame, 
                text=status_text, 
                text_color=status_color,
                font=("Helvetica", 12, "bold")
            )
            status_label.grid(row=row, column=3, padx=10, pady=5, sticky="w")
            
            # Action buttons frame
            action_frame = Ctk.CTkFrame(self.scrollable_frame)
            action_frame.grid(row=row, column=4, padx=10, pady=5, sticky="ew")
            action_frame.grid_columnconfigure((0, 1, 2), weight=1)
            
            # Toggle button
            toggle_text = "Deactivate" if indicator["active"] else "Activate"
            toggle_color = "firebrick3" if indicator["active"] else "forest green"
            toggle_hover = "firebrick4" if indicator["active"] else "dark green"
            
            toggle_btn = Ctk.CTkButton(
                action_frame,
                text=toggle_text,
                width=80,
                fg_color=toggle_color,
                hover_color=toggle_hover,
                command=lambda seq=indicator["sequence"]: self.toggle_indicator_status(seq)
            )
            toggle_btn.grid(row=0, column=0, padx=5, pady=0)
            
            # Edit button
            edit_btn = Ctk.CTkButton(
                action_frame,
                text="Edit",
                width=60,
                command=lambda seq=indicator["sequence"]: self.edit_indicator(seq)
            )
            edit_btn.grid(row=0, column=1, padx=5, pady=0)
            
            # Remove button
            remove_btn = Ctk.CTkButton(
                action_frame,
                text="Remove",
                width=60,
                fg_color="firebrick3",
                hover_color="firebrick4",
                command=lambda seq=indicator["sequence"]: self.remove_indicator(seq)
            )
            remove_btn.grid(row=0, column=2, padx=5, pady=0)
    
    def get_config(self):
        """Get all indicator configurations as a dictionary"""
        return {
            "indicators": self.indicators
        }
    
    def set_config(self, config_dict):
        """Set values from a dictionary"""
        if "indicators" in config_dict:
            self.indicators = config_dict["indicators"]
            # Add active field if not present in loaded config (backward compatibility)
            for indicator in self.indicators:
                if "active" not in indicator:
                    indicator["active"] = True
            # Update the sequence counter
            if self.indicators:
                self.current_sequence = max(ind["sequence"] for ind in self.indicators)
            else:
                self.current_sequence = 0
            # Update the display
            self.update_indicator_list()