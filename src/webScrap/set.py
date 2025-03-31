from datetime import datetime

class Set:
    def __init__(self, name: str, link: str, release_date: datetime):
        self.name = name
        self.link = link
        self.release_date = release_date

    def __str__(self):
        return f'name: {self.name}\nlink: {self.link}\nrelease_date: {self.release_date}'