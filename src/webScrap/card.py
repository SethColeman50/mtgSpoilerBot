class Card:
    def __init__(self, name: str, image_link: str, oracle_text: str, set_name: str):
        self.name = name
        self.image_link = image_link
        self.oracle_text = oracle_text
        self.set_name = set_name
        
    def __str__(self):
        return f'name: {self.name}\nimage_link: {self.image_link}\noracle_text: {self.oracle_text}\nset_name: {self.set_name}'