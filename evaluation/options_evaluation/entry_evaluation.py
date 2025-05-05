    set_active = redis.get..
    start_time = redis.get..
    end_time = redis.get...
    entry_time_exclusion = redis.get...
    exit time exclusions = 
    trade_active_status = redis.get flags['tradestatus']
    indicators_conditions_status = redis
    entry_conditions_refresh = redis.get
    exit_conditions_refresh = rdis.get 
    entry_order_status = redis.
    
    while entry_order_status == False :
        if indicators_conditions_status is True :
            entry_success_status  = execute_entry_order () 
        

        