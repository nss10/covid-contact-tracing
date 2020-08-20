from enum import IntEnum
import json

class Room():
    def __init__(self, id, name, max_capacity, last_sanitized_time=None, current_strength=None):
        self.id=id
        self.name=name
        self.max_capacity=max_capacity
        self.last_sanitized_time=last_sanitized_time
        self.current_strength=current_strength
    def __str__(self):
        return f"Room({self.id},{self.name},{self.max_capacity},{self.last_sanitized_time},{self.current_strength})"

class Status(IntEnum):
    ENTRY = 1
    EXIT = 0

class SanitizedStatus(IntEnum):
    IN_PROGRESS=1
    CLEAN=0

class Event():
    def __init__(self, user_id, room_id, status, timestamp):
        self.user_id = user_id
        self.room_id = room_id
        self.status = Status.ENTRY if int(status) == 1 else Status.EXIT 
        self.timestamp = timestamp
    def __str__(self):
        return f"Event({self.user_id},{self.room_id}, {self.status}, {self.timestamp})"


class SanitizedEvent(Event):
    def __init__(self, user_id, room_id, status, timestamp):
        super().__init__(user_id, room_id,status,timestamp)
        self.status = SanitizedStatus.IN_PROGRESS if status else SanitizedStatus.CLEAN
    def __str__(self):
        return f"SanitizedEvent({self.user_id},{self.room_id}, {self.status}, {self.timestamp})"

class Window():
    """ A window is a time frame   """
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __hash__(self):
        return hash((self.start, self.end))

    def __str__(self):
        return "(" + str(self.start.replace(microsecond=0).isoformat()) + " to " + str(self.end.replace(microsecond=0).isoformat()) +")"

class UserVisitWindow(Window):
    def __init__(self, user_id, start, end):
        self.user_id = user_id
        super().__init__(start, end)

    def __str__(self):
        return "[ user-id: " + str(self.user_id) + ", "+ Window.__str__(self) +" ]"

class Overlap():
    """ Represents the overlap of two time frames (Windows) """
    def __init__(self, room_id, agent_visit_window, user_visit_window):
        self.room_id = room_id
        self.agent_visit_window = agent_visit_window
        self.user_visit_window = user_visit_window
        self.overlap_index = self.__compute_overlap_index()

    def __str__(self):
        return "room_id: " + self.room_id + " agent-window : " +str(self.agent_visit_window) +" user-window : " +str(self.user_visit_window)+"\n"
    
    def __eq__(self,other):
        return self.room_id==other.room_id and \
            hash(self.agent_visit_window)==hash(other.agent_visit_window) and \
             hash(self.user_visit_window)==hash(other.user_visit_window)
                
    def __hash__(self):
        return hash((self.room_id, self.agent_visit_window, self.user_visit_window))       

    def __compute_overlap_index(self):
        return 0

