import customtkinter as Ctk

class Configure(Ctk.CTkFrame):
    def __init__(self, parent, shared_dicts):
        super().__init__(parent)
        self.shared_dicts = shared_dicts  # Store the shared dictionaries

        title_label = Ctk.CTkLabel(self, text="Configure", font=("Arial", 24, "bold"))
        title_label.pack(pady=20)

        # ----- Placeholder Widgets -----

        placeholder_label = Ctk.CTkLabel(self, text="This is a placeholder label.")
        placeholder_label.pack(pady=10)

        placeholder_entry = Ctk.CTkEntry(self, placeholder_text="Enter some text...")
        placeholder_entry.pack(pady=10)

        placeholder_slider = Ctk.CTkSlider(self, from_=0, to=100)
        placeholder_slider.pack(pady=10)

        placeholder_checkbox = Ctk.CTkCheckBox(self, text="Enable something")
        placeholder_checkbox.pack(pady=10)

        placeholder_button = Ctk.CTkButton(self, text="Save Settings")
        placeholder_button.pack(pady=20)

        # ----- Light/Dark Mode Toggle -----
        mode_switch = Ctk.CTkSwitch(self, text="Light mode", command=self.toggle_mode)
        mode_switch.pack(pady=20)
        mode_switch.select()  # Default to dark mode

    def toggle_mode(self):
        current_mode = Ctk.get_appearance_mode()
        new_mode = "Light" if current_mode == "Dark" else "Dark"
        Ctk.set_appearance_mode(new_mode)

