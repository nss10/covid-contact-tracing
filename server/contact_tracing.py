from db_interface import fetch_overlapped_users, fetch_rooms_visited
from helper import  get_infected_window
from enum import IntEnum


class Status(IntEnum):
    ENTRY = 1
    EXIT = 0

class Event():

    def __init__(self, user_id, room_id, status, timestamp):
        self.user_id = user_id
        self.room_id = room_id
        self.status = Status.ENTRY if status else Status.EXIT 
        self.timestamp = timestamp

class Window():
    """ A window is a time frame   """
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __hash__(self):
        return hash((self.start, self.end))

class UserVisitWindow(Window):
    def __init__(self, user_id, start, end):
        self.user_id = user_id
        super().__init__(start, end)

class InfectedWindows():
    """
        Similar to an iterator design patter, this class has a dictionary of all the infected windows, 
        with key being the hashcode of the window
    """

    class InfectedWindow(Window):
        """ Given a visited window finds an infected window for that particular visit. Also contains all visited windows that fall within this"""
        def __init__(self, visit_window):
            window = get_infected_window(visit_window)
            super().__init__(window.start, window.end)
            self.agent_visit_windows = []
        def add_agent_visit_window(self, visit_window):
        # Adds a visit window for this infected window
            self.agent_visit_windows.append(visit_window)
        def get_agent_visits(self):
            return self.agent_visit_windows
    def __init__(self):
        self.infected_windows = {}

    def get(self, window):
        if window not in self.infected_windows:
            self.infected_windows[window] = self.InfectedWindow(window)
        return self.infected_windows[window]
    
    def __iter__(self):
        return iter(self.infected_windows.values())

class Overlap():
    """ Represents the overlap of two time frames (Windows) """
    def __init__(self, room_id, agent_visit_window, user_visit_window):
        self.room_id = room_id
        self.agent_visit_window = agent_visit_window
        self.user_visit_window = user_visit_window
        self.overlap_index = self.__compute_overlap_index()
    def __compute_overlap_index(self):
        return 0

class RoomVisits():
    class RoomVisit():
        def __init__(self, room_id):
            self.room_id = room_id
            self.agent_visits = []
            self.user_visits = []
            self.infected_windows = InfectedWindows()

        def add_agent_visit(self, entry_timestamp, exit_timestamp):
            visit_window = Window(entry_timestamp, exit_timestamp)
            self.agent_visits.append(visit_window)
            self.infected_windows.get(visit_window).add_agent_visit_window(visit_window)

        def add_user_visit(self, user_id, entry_timestamp, exit_timestamp):
            user_visit_window = UserVisitWindow(user_id, entry_timestamp, exit_timestamp)
            self.user_visits.append(user_visit_window)

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
            self.total_overlap_index = 0
            self.overlap_frequency = 0

        def add_overlap(self, overlap):
            self.overlaps.append(overlap)
            self.total_overlap_index += overlap.overlap_index
            self.overlap_frequency+=1

    def __init__(self):
        self.users = {}

    def get(self, user_id):
        if user_id not in self.users:
            self.users[user_id] = self.OverlappedUser(user_id)
        return self.users[user_id]

    def __iter__(self) :
        return iter(self.users.values())
