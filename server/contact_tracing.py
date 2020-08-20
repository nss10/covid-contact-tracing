from entities import Event, Window, UserVisitWindow
from db_interface import get_infected_window
class InfectedWindows():
    """
        Similar to an iterator design patter, this class has a dictionary of all the infected windows, 
        with key being the hashcode of the window
    """

    class InfectedWindow(Window):
        """ Given a visited window finds an infected window for that particular visit. Also contains all visited windows that fall within this"""
        def __init__(self, room_id, visit_window):
            window = get_infected_window(room_id, visit_window)
            super().__init__(window.start, window.end)
            self.agent_visit_windows = []
        def add_agent_visit_window(self, visit_window):
        # Adds a visit window for this infected window
            self.agent_visit_windows.append(visit_window)
        def get_agent_visits(self):
            return self.agent_visit_windows
    def __init__(self,room_id):
        self.infected_windows = {}
        self.room_id = room_id

    def get(self, window):
        if window not in self.infected_windows:
            self.infected_windows[window] = self.InfectedWindow(self.room_id, window)
        return self.infected_windows[window]
    
    def __iter__(self):
        return iter(self.infected_windows.values())

class RoomVisits():
    class RoomVisit():
        def __init__(self, room_id):
            self.room_id = room_id
            self.agent_visits = []
            self.user_visits = []
            self.infected_windows = InfectedWindows(self.room_id)

        def add_agent_visit(self, entry_timestamp, exit_timestamp):
            visit_window = Window(entry_timestamp, exit_timestamp)
            self.agent_visits.append(visit_window)
            self.infected_windows.get(visit_window).add_agent_visit_window(visit_window)

        def add_user_visit(self, user_id, entry_timestamp, exit_timestamp):
            user_visit_window = UserVisitWindow(user_id, entry_timestamp, exit_timestamp)
            self.user_visits.append(user_visit_window)

        def __str__(self):
            return str(self.room_id) + " - [" + ", ".join([str(agent_visit) for agent_visit in self.agent_visits]) +"]\n" \
                        + "Infected windows" + " - [" + ", ".join([str(infected_window) for infected_window in self.infected_windows]) +"]\n"  \
                         + "User Visits" + " - [" + ", ".join([str(user_visit) for user_visit in self.user_visits]) +"]\n" 

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
            if overlap not in self.overlaps:
                self.overlaps.append(overlap)
                self.total_overlap_index += overlap.overlap_index
                self.overlap_frequency+=1

        def __str__(self):
            retVal = "user_id: " +str(self.user_id) +"\nOverlap_frequency: "+ str(self.overlap_frequency) +"\n total_overlap_index: "+ str(self.total_overlap_index) +"\n\tOverlaps:\n"
            for overlap in self.overlaps:
                retVal+=str(overlap)
            return retVal
            
            
    def __init__(self):
        self.users = {}

    def get(self, user_id):
        if user_id not in self.users:
            self.users[user_id] = self.OverlappedUser(user_id)
        return self.users[user_id]

    def __iter__(self) :
        return iter(self.users.values())


