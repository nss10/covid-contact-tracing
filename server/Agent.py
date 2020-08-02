from helper import compute_overlap_index
from db_interface import fetch_rooms_visited
class Agent():

    class RoomVisits():
        class RoomVisit():
            def __init__(self, room_id):
                self.room_id = room_id
                self.visits = []

            def add_visit(self, entry_timestamp, exit_timestamp):
                self.visits.append((entry_timestamp, exit_timestamp))

        def __init__(self):
            self.rooms = {}

        def get(self, room_id):
            if room_id not in self.rooms:
                self.rooms[room_id] = self.RoomVisit(room_id)
            return self.rooms[room_id]

        #TODO: Add iterator for Room visits 




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

        # TODO: Add iterator for Overlapped users


    def __init__(self, user_id):
        self.user_id = user_id
        self.room_visits = self.populate_room_visits()
        self.overlapped_users = self.populate_overlapped_users()

    def populate_room_visits(self):
        room_visits = self.RoomVisits()
        events = fetch_rooms_visited(self.user_id)
        for entry_event, exit_event in zip(events[0::2], events[1::2]):
            room_visits.get(entry_event['room_id']).add_visit(entry_event['timestamp'], exit_event['timestamp'])
        return room_visits

    def populate_overlapped_users(self):
        overlap_users = self.OverlappedUsers()
        room_visits = self.room_visits
        # TODO: 
            # for each timestamp for a room, get before and after sanitized times
                # fetch all events between the sanitized times
                #filter all events with both entry and exit before agent entry event
                #from the remaining events, find entry and exit pairs and create overlap object
                #add the overlap object to the overlapped user with the user_id fetched from the events
                    #overlap_users.get(user_id).add_overlap(overlap)
            # return overlap_users
        return []

    