from datetime import datetime as dt
def room_entry(event):
    event={"code":"1432-0","uid":"2309","ts":dt(2020,4,23,16,23,34,123)}
    room_id,status=event['code'].split('-')
    user_id,timeStamp=event['uid'],event['ts']
    print(room_id,user_id,timeStamp,status)
    isJanitor(user_id)
    #Add event info to db
    
    #Update room capacity
    update_room_capacity(event)
    #IF event type is entry
        #Return room name and last sanitized time
    #Else
        #Return time spent in the room
    '''
    if(status ==0):
        return fetch_room_info(event.room_id)
    else:
        return fetch_time_spent(event.user_id, event.room_id)
    '''
def add_sanitized_event(sanitize_event):
    pass

def update_room_capacity(event):
    pass


def isJanitor(uid):
    pass



if __name__ == "__main__":
    room_entry(None)