# main.py
import customtkinter as Ctk
import json
import os
from ui.app import App  # Your main app class

# Set customtkinter appearance
Ctk.set_appearance_mode("dark")
Ctk.set_default_color_theme("green")

# Load dictionaries from JSON files in utils folder
def load_json(file_name):
    file_path = os.path.join("utils", file_name)
    with open(file_path, "r") as f:
        return json.load(f)

credentials = load_json("credentials.json") # Initialize the four dictionaries
shared_dicts = {"credentials": credentials,}    # Bundle dictionaries for easy passing


if __name__ == "__main__":

    app = App(shared_dicts) 
    app.mainloop()