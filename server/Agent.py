from helper import get_unsanitized_windows
from db_interface import fetch_rooms_visited, fetch_events_in_window
from contact_tracing import Overlap, RoomVisits, OverlappedUsers
class Agent():
    def __init__(self, user_id):
        self.user_id = user_id
        self.room_visits = self.populate_room_visits()
        self.overlapped_users = self.populate_overlapped_users()

    def populate_room_visits(self):
        room_visits = RoomVisits()
        events = fetch_rooms_visited(self.user_id) #TODO: implementation needed
        for entry_event, exit_event in zip(events[0::2], events[1::2]):
            room_visits.get(entry_event['room_id']).add_visit(entry_event['timestamp'], exit_event['timestamp'])
        return room_visits

    def populate_overlapped_users(self):
        overlap_users = OverlappedUsers()
        room_visits = self.room_visits
        # TODO: 
            # for each timestamp for a room, get before and after sanitized times
        for room in room_visits:
            # fetch all events between the sanitized times
                for unsanitized_window in room.unsanitized_windows :
                    events = fetch_events_in_window(unsanitized_window)
                #filter all events with both entry and exit before agent entry event
                #from the remaining events, find entry and exit pairs and create overlap object
                #add the overlap object to the overlapped user with the user_id fetched from the events
                    #overlap_users.get(user_id).add_overlap(overlap)
            # return overlap_users
        return []

    