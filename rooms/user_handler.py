from .user import User

class UserHandler():
    def __init__(self):
        self.users = []

    def add_user(self, ip:str):
        """adds a user"""
        
        self.users.append(User(ip))