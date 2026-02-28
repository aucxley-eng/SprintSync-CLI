from models.person import Person

class User(Person):
    def __init__(self, name: str, role: str = "Member"):
        super().__init__(name)
        self.role = role
        self.is_logged_in = False