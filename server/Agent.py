from db_interface import fetch_visit_events_of_user, fetch_events_in_window, get_infected_window
from entities import Overlap, Status
from contact_tracing import RoomVisits, OverlappedUsers
from operator import attrgetter

class Agent():
    def __init__(self, user_id):
        self.user_id = user_id
        self.room_visits = self.populate_room_visits()
        self.overlapped_users = self.populate_overlapped_users()
        
    def populate_room_visits(self):
        room_visits = RoomVisits()
        events = fetch_visit_events_of_user(self.user_id) #TODO: implementation needed
        for entry_event, exit_event in zip(events[0::2], events[1::2]):
            room_visits.get(entry_event.room_id).add_agent_visit(entry_event.timestamp, exit_event.timestamp)
        return room_visits

    def populate_overlapped_users(self):
        overlapped_users = OverlappedUsers()
        for room in self.room_visits:
                for infected_window in room.infected_windows :
                    events = fetch_events_in_window(room.room_id, infected_window) 
                    self.populate_user_visit_windows(room, events, infected_window)
                #from the visit windows create , create overlap object -- iterate through room.user_visits
                for user_visit in room.user_visits:
                #Fetch the overlapped user with the user_id fetched from the events
                    overlapped_user = overlapped_users.get(user_visit.user_id)
                    for agent_visit in room.agent_visits:
                        if(user_visit.end >= agent_visit.start): # If he falls in potential infectant window
                            overlapped_user.add_overlap(Overlap(room.room_id, agent_visit, user_visit))
        return overlapped_users

    
    def populate_user_visit_windows(self, room, events, infected_window):
        events = sorted(events, key = attrgetter('user_id','timestamp')) # Sort them with user_ids and timestamps, to make an entry exit pair
        for entry_event, exit_event in zip(events[0::2], events[1::2]):
            #filter agent events and all other events with both entry and exit before agent's first entry
            if(entry_event.user_id == self.user_id or exit_event.timestamp < infected_window.get_agent_visits()[0].start):
                continue
            if(entry_event.user_id != exit_event.user_id):
                print("Error")
            self.room_visits.get(entry_event.room_id).add_user_visit(entry_event.user_id, entry_event.timestamp, exit_event.timestamp)

if __name__ == "__main__":
    agent = Agent(54860)
    for ou in agent.overlapped_users:
            print(ou)
    # for rv in agent.room_visits:
        # print("Room - "+rv.room_id)
        # print("Agent Visits")
        # for av in rv.agent_visits:
        #     print(av)
        # print("Infected Windows")
        # for iw in rv.infected_windows:
        #     print(iw)
        # print("User Visits")
        # for uv in rv.user_visits:
        #     print(uv)
        
        
    