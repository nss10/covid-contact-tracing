from db_interface import fetch_overlapped_users, fetch_rooms_visited
from helper import compute_overlap_index, get_unsanitized_window




class Window():
    def __init__(self, start=None, end=None, window=None):
        self.start = start
        self.end = end

    def __hash__(self):
        return hash((self.start, self.end))

class UnsanitizedWindow(Window):
    def __init__(self, visited_window):
        unsanitized_window = get_unsanitized_window(visit_window) #FIXME: WIP
        super(window = unsanitized_window)
        self.visted = []

class Overlap():
    def __init__(self, room_id, agent_visit_window, user_visit_window):
        self.room_id = room_id
        self.agent_visit_window = agent_visit_window
        self.user_visit_window = user_visit_window

class RoomVisits():
    class RoomVisit():
        unsanitized_windows = {}
        def __init__(self, room_id):
            self.room_id = room_id
            self.visits = []
        def add_visit(self, entry_timestamp, exit_timestamp):
            visit_window = Window(entry_timestamp, exit_timestamp)
            self.visits.append(visit_window)
            #self.unsanitized_windows.add(visit_window.unsanitized_window) #FIXME: WIP

    def __init__(self):
        self.rooms = {}

    def get(self, room_id):
        if room_id not in self.rooms:
            self.rooms[room_id] = self.RoomVisit(room_id)
        return self.rooms[room_id]


    def __iter__(self) :
        return iter(self.rooms.values())



class OverlappedUsers():
    class OverlappedUser():
        def __init__(self, user_id):
            self.user_id = user_id
            self.overlaps = []
            self.overlapIndex = 0
            self.overlapFrequency = 0

        def add_overlap(self, overlap):
            self.overlaps.append(overlap)
            self.overlapIndex += compute_overlap_index(overlap)
            self.overlapFrequency+=1

    def __init__(self):
        self.users = {}

    def get(self, user_id):
        if user_id not in self.users:
            self.users[user_id] = self.OverlappedUser(user_id)
        return self.users[user_id]

    def __iter__(self) :
        return iter(self.users.values())
