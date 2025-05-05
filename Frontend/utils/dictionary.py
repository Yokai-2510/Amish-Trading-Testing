import json

def generate_strategy_set(set_number):
    return {
        f"set{set_number}": {

            "set_config": {
                "set_name": f"Set{set_number}",
                "set_active_status": False,
                "broker": "upstox",
                "start_time": "HH:MM:SS",
                "end_time": "HH:MM:SS",
            },

            "options_config": {
                "option_index": "nifty",
                "option_type": "CE" ,
                "trade_type": "BUY" ,
                "strike_selection": "ITM",
                "strike_value": 5 ,
                "quantity_lots": 10 ,
                "expiry": "3/6/2025"
            },

            "entry_conditions": {},

            "exit_conditions": {},

            "entry_config": {
                "chart_type": "Heiken Ashi",
                "time_frame": "15m",
                "entry_refresh_interval": 2,
                "time_exclusion": {"from_time": "10:00", "to_time": "12:00"}
            },

            "exit_config": {
                "chart_type": "Candlestick",
                "time_frame": "15m",
                "exit_refresh_interval": 1,
                "stop_loss": {
                    "type": "Percentage",
                    "value": 2.5 ,
                    "max_per_day": 5,
                    "max_per_trade": 2,
                    "time_based": 30
                },
                "target": {"type": "Price", "value": "5"}
            }
        }
    }

def generate_strategy_options():
    strategy_options = {}
    for i in range(1, 9):
        strategy_options.update(generate_strategy_set(i))
    
    with open('strategy_options.json', 'w') as f:
        json.dump(strategy_options, f, indent=4)
    print("JSON file 'strategy_options.json' has been created.")

if __name__ == "__main__":
    generate_strategy_options()


