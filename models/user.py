from models.person import Person
from utils.auth_tools import hash_password

class User(Person):
    def __init__(self, name: str, email: str, password: str, role: str = 'user') -> None:
        super().__init__(name, email)
        self.password_hash = hash_password(password)
        self.role = role

    def verify_password(self, password: str) -> bool:
        return self.password_hash == hash_password(password)

    def to_dict(self) -> dict[str, str]:
        return {
            "name": self.name,
            "email": self.email,
            "password_hash": self.password_hash,
            "role": self.role
        }
