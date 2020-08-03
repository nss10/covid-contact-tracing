import random
from datetime import datetime, timedelta

base = datetime(2020, 1, 22, 00, 00, 00)
def gen_un(num=10):
     return [random.randint(10001,99999) for i in range(num)]

def gen_rid(num=10):
     return [chr(65 + random.randint(0,25)) + str(random.randint(10001,99999)) for i in range(num)]

# or a function
def gen_datetime(base,endTime=False):
    # generate a datetime in format yyyy-mm-dd hh:mm:ss.000000
    daysLimit = 0 if endTime else 10
    base += timedelta(days=random.randint(0,daysLimit), hours=random.randint(0,10), minutes=random.randint(1,30), seconds=random.randint(0,10), microseconds=random.randint(0,100000))
    return base

class Event():
    def __init__(self, user_id, room_id, status, timestamp):
        self.user_id = user_id
        self.room_id = room_id
        self.status = status
        self.timestamp = timestamp
    
    def __str__(self):
        return f"Event({self.user_id},{self.room_id}, {self.status}, {self.timestamp})"
    
def get_entry_exit_pairs(user_id,ridList, num=100):
    events = []
    start = base
    for i in range(num):
        room_id = ridList[random.randint(0,len(ridList)-1)]
        start = gen_datetime(start)
        if(start>=datetime.now()):
            break
        end = gen_datetime(start, True)
        events.append(Event(user_id,room_id, 1, start))
        events.append(Event(user_id,room_id, 0, end))
        start=end
    return events
    
def addToFile(events, fname):
        f = open("mockdata/"+fname,"w")
        for event in events:
            f.write(str(event)+"\n")


def main():
    global base
    unList = gen_un(10)
    ridList = gen_rid(10)
    all_events=[]
    for un in unList:
        base = datetime(2020, 1, 22, 00, 00, 00)
        all_events+=(get_entry_exit_pairs(un, ridList,30))
    
    all_events.sort(key=lambda event:event.user_id)
    addToFile(all_events,"events-user_id.txt")
    all_events.sort(key=lambda event:event.room_id)
    addToFile(all_events,"events-room_id.txt")
    all_events.sort(key=lambda event:event.timestamp)
    addToFile(all_events,"events-timestamp.txt")
    
    return all_events


if __name__ == "__main__":
    main()