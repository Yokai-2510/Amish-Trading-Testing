import customtkinter as Ctk

class Connect(Ctk.CTkFrame):
    def __init__(self, parent, shared_dicts):
        super().__init__(parent)
        self.shared_dicts = shared_dicts  # Store the shared dictionaries
        
        # Main label
        label = Ctk.CTkLabel(self, text="Connect", font=("Arial", 24, "bold"))
        label.pack(pady=20)
        
        # Create tabview
        self.tabview = Ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Create tabs
        self.tab_upstox = self.tabview.add("Upstox")
        self.tab_zerodha = self.tabview.add("Zerodha")
        self.tab_kotak = self.tabview.add("Kotak")
        self.tab_fyers = self.tabview.add("Fyers")
        
        # Initialize each tab's content
        self.setup_upstox_tab()
        self.setup_zerodha_tab()
        self.setup_kotak_tab()
        self.setup_fyers_tab()
    
    def create_entry_field(self, parent, label_text, row):
        """Helper function to create consistent entry fields"""
        label = Ctk.CTkLabel(parent, text=label_text)
        label.grid(row=row, column=0, padx=10, pady=5, sticky="w")
        
        entry = Ctk.CTkEntry(parent, width=300)
        entry.grid(row=row, column=1, padx=10, pady=5, sticky="ew")
        
        return entry
    
    def create_status_label(self, parent, row):
        """Helper function to create connection status label"""
        status_frame = Ctk.CTkFrame(parent)
        status_frame.grid(row=row, column=0, columnspan=2, pady=10)
        
        status_label = Ctk.CTkLabel(status_frame, text="Connection Status:")
        status_label.pack(side="left", padx=5)
        
        status = Ctk.CTkLabel(status_frame, text="Inactive", text_color="red")
        status.pack(side="left")
        
        return status
    
    def create_button_frame(self, parent, row):
        """Helper function to create button frame with Save and Connect buttons"""
        button_frame = Ctk.CTkFrame(parent)
        button_frame.grid(row=row, column=0, columnspan=2, pady=10)
        
        save_btn = Ctk.CTkButton(button_frame, text="Save Configuration")
        save_btn.pack(side="left", padx=10)
        
        connect_btn = Ctk.CTkButton(button_frame, text="Connect API to Broker")
        connect_btn.pack(side="left", padx=10)
        
        return save_btn, connect_btn
    
    def setup_upstox_tab(self):
        """Setup Upstox configuration fields"""
        frame = Ctk.CTkFrame(self.tab_upstox)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        frame.grid_columnconfigure(1, weight=1)
        
        self.upstox_api_key = self.create_entry_field(frame, "API Key:", 0)
        self.upstox_api_secret = self.create_entry_field(frame, "API Secret:", 1)
        self.upstox_totp_key = self.create_entry_field(frame, "TOTP Key:", 2)
        self.upstox_redirect_url = self.create_entry_field(frame, "Redirect URL:", 3)
        self.upstox_pin = self.create_entry_field(frame, "PIN:", 4)
        self.upstox_mobile_number = self.create_entry_field(frame, "Mobile Number:", 5)
        
        self.upstox_status = self.create_status_label(frame, 6)
        self.upstox_save_btn, self.upstox_connect_btn = self.create_button_frame(frame, 7)
    
    def setup_kotak_tab(self):
        """Setup Kotak configuration fields"""
        frame = Ctk.CTkFrame(self.tab_kotak)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        frame.grid_columnconfigure(1, weight=1)
        
        self.kotak_password = self.create_entry_field(frame, "Kotak Password:", 0)
        self.kotak_mpin = self.create_entry_field(frame, "MPIN:", 1)
        self.kotak_consumer_key = self.create_entry_field(frame, "Consumer Key:", 2)
        self.kotak_consumer_secret = self.create_entry_field(frame, "Consumer Secret:", 3)
        
        self.kotak_status = self.create_status_label(frame, 4)
        self.kotak_save_btn, self.kotak_connect_btn = self.create_button_frame(frame, 5)
    
    def setup_zerodha_tab(self):
        """Setup Zerodha configuration fields"""
        frame = Ctk.CTkFrame(self.tab_zerodha)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        frame.grid_columnconfigure(1, weight=1)
        
        self.zerodha_api_key = self.create_entry_field(frame, "API Key:", 0)
        self.zerodha_api_secret = self.create_entry_field(frame, "API Secret:", 1)
        self.zerodha_user_id = self.create_entry_field(frame, "User ID:", 2)
        self.zerodha_user_password = self.create_entry_field(frame, "User Password:", 3)
        self.zerodha_totp_key = self.create_entry_field(frame, "TOTP Key:", 4)
        
        self.zerodha_status = self.create_status_label(frame, 5)
        self.zerodha_save_btn, self.zerodha_connect_btn = self.create_button_frame(frame, 6)
    
    def setup_fyers_tab(self):
        """Setup Fyers configuration fields"""
        frame = Ctk.CTkFrame(self.tab_fyers)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        frame.grid_columnconfigure(1, weight=1)
        
        self.fyers_username = self.create_entry_field(frame, "Username (Fyers ID):", 0)
        self.fyers_totp_key = self.create_entry_field(frame, "TOTP Key/Password:", 1)
        self.fyers_pin = self.create_entry_field(frame, "PIN:", 2)
        self.fyers_client_id = self.create_entry_field(frame, "Client ID:", 3)
        self.fyers_secret_key = self.create_entry_field(frame, "Secret Key:", 4)
        self.fyers_redirect_uri = self.create_entry_field(frame, "Redirect URI:", 5)
        
        self.fyers_status = self.create_status_label(frame, 6)
        self.fyers_save_btn, self.fyers_connect_btn = self.create_button_frame(frame, 7)