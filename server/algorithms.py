from datetime import datetime as dt
from db_interface import *


def room_entry(event):
    room_id, status = event['code'].split('-')
    user_id, timeStamp = event['uid'], event['ts']
    # print(room_id,user_id,timeStamp,status)
    room_info = fetch_room_info(room_id)
    if isJanitor(user_id):
        room_info['clean_prompt'] = 1
    else:
        handle_missing_events(room_id, user_id, status, timeStamp)

        add_event(event)
        update_room_capacity(room_id, user_id, status)
    return room_info


def room_exit(event):
    room_id, status = event['code'].split('-')
    user_id, timeStamp = event['uid'], event['ts']
    if isJanitor(user_id):
        room_clean_exit(event)
    else:
        handle_missing_events(user_id, room_id, status, timeStamp)
        add_event(event)
        update_room_capacity(room_id, user_id, status)
        return {"code": 200, "status": "Success"}


def update_room_capacity(room_id, user_id, status):
    current_capacity = fetch_room_info(room_id)['current_capacity']
    if status == 0:
        set_room_capacity(room_id, current_capacity-1)
    else:
        set_room_capacity(room_id, current_capacity+1)


def isJanitor(uid):
    pass


def handle_missing_events(room_id, user_id, status, timeStamp):
    old_rec = fetch_last_user_record(room_id, user_id)
    #WIP
    if status == 0:  # room exit
        if old_rec['status'] == 0:  # Missing current room entry
            return {"message": "Missing current room entry", [{"room_id": room_id, "proposed_time": dt.strptime(timeStamp) + dt.timedelta(minutes=30)}]}
        # Missing current room entry and old room exit
        elif old_rec['status'] == 1 and old_rec['room_id'] != room_id:
            return {\
                        "message": "Missing current room entry",
                        "info" :[ \
                                    {"room_id": room_id, "proposed_time": dt.strptime(timeStamp) + dt.timedelta(minutes=30)}, \
                                    {"room_id": old_rec['room_id'], "proposed_time": dt.strptime(old_rec['timeStamp']) + dt.timedelta(minutes=-30)} \
                                ] \
                    }


def room_clean(event):
    room_id, status = event['code'].split('-')
    timeStamp = event['ts']
    add_sanitized_event(event)
    if status == 0:
        set_last_sanitized_ts(room_id, timeStamp)
    else:
        set_last_sanitized_ts(room_id, ts=None)


def room_clean_exit(event):
    room_id = event['code'].split('-')[0]
    add_sanitized_event(event)
    set_last_sanitized_ts(room_id, ts=None)


if __name__ == "__main__":
    event = {"code": "1432-0", "uid": "2309",
             "ts": dt(2020, 4, 23, 16, 23, 34, 123)}
    room_entry(event)
