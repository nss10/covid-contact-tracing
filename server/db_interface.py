from datetime import datetime as dt
def fetch_room_info(room_id):
    #return room{name, last_sanitized_time}
    return {"name":"pilion hall", "last_sanitized_time":dt(2020,4,23,19,13,34,123), "current_capacity":14, "max_capacity":20}

def fetch_last_user_record(user_id, room_id):
    #Fetch the last event with user_id and room_id with status as 'Entry'
    return {"rid":room_id,"uid":user_id,"status":0,"timestamp":dt(2020,4,23,19,13,34,123)}

def add_event(event):
    #Insert this record in events collection
    pass

def add_sanitized_event(event):
    #Insert this record in sanitized events collection
    pass

def set_room_capacity(room_id, capacity):
    pass

def set_last_sanitized_ts(room_id,ts):
    if ts==None:
        pass #insert ts = "Cleaning in progress"
    else:   
        pass #insert ts = given timestamp for that room

def fetch_rooms_visited(user_id):
    return [] #rooms

def fetch_overlapped_users(user_id, room_id, timestamp):
    return [] #List of user objects