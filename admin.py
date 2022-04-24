class Admins():
    """handels admins and contains the admin password"""
    def __init__(self, password:str):
        self.password = password

        self.admins = set()

    def is_admin(self, ip:str) -> bool:
        return ip in self.admins

    def add_admin(self, ip):
        self.admins.add(ip)