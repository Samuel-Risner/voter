from .room import Room

class RoomHandler():
    def __init__(self):
        self.open_rooms = {}
        self.closed_rooms = {}
        self.closed_rooms_count = 0

    def open_room(self, room_name:str) -> bool:
        """True if room could bbe opened
        False if it could not be opened"""

        # already opened
        if room_name in self.open_rooms:
            return False
        # opened room
        else:
            self.open_rooms[room_name] = Room(room_name)
            return True

    def add_user(self, room_name, ip) -> tuple:
        """first part of the tuple:
        True if room is opened, False if it is not
        second part
            corresponding room-object
            None if error"""

        # if the room is opened
        if room_name in self.open_rooms:
            room = self.open_rooms[room_name]
            room.add_user(ip)
            return (True, room)
            
        else:
            return (False, None)

    def close_room(self, room_name:str):
        """closes an opened room
        and saves the results from voting"""

        room = self.open_rooms.pop(room_name)

        self.closed_rooms[self.closed_rooms_count] = room
        self.closed_rooms_count += 1

        room.load_results_html()

    def get_room(self, room_name:str) -> Room:
        """returns the Room-object if the room is opened, None if it is not"""

        if room_name in self.open_rooms: # is opened
            return self.open_rooms[room_name]

        else: # is not opened
            return None

    def get_opened_rooms(self) -> list:
        """return the names from the opened rooms"""

        x = []

        for i in self.open_rooms:
            x.append(i)

        return x

    def get_closed_rooms(self) -> list:
        """return the names from the closed rooms"""

        x = []
        for i in self.closed_rooms.items():
            x.append(i[1].name)

        return x

    def add_result(self, room_name, result) -> bool:
        """False: room is not opened
        True: result was added"""

        # if room is not opened
        if room_name not in self.open_rooms:
            return False

        room = self.get_room(room_name)
        room.add_result(result)
        return True