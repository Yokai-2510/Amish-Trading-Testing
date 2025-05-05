from indicators.entry_indicators import update_entry_indicators
from indicators.exit_indicators import update_exit_indicators
import time 

def process_indicators () : 
    
    print ("Processing Indicators : " ) 
    print ("Started Calculation of Entry Indicators")

    while True : 
        update_entry_indicators()
        update_exit_indicators()
        time.sleep(1)
# Indicators will be met once criteria is met again , if already criteria met , no active condition signal 