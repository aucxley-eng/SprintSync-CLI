import hashlib
import os
import json
from jsonschema import validate, ValidationError

schema = {
    "type": "object",
    "properties": {
        "id": {"type": "number"},
        "username": {"type": "string"},
        "password": {"type": "string"},
        "role": {"type": "string"}
    },
    "required": ["username", "password", "role"]
}

current_user = None

FILE_BASE = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(FILE_BASE, "data")
FILE_PATH = os.path.join(DATA_DIR, "users.json")


def hash_password(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, hashed_password: str) -> bool:
        return hash_password(password) == hashed_password


def load_user():
        try:
                with open(FILE_PATH, "r") as file:
                        return json.load(file)
        except PermissionError:
                print("Access denied")
                return []


def add_users(new_user):
            with open(FILE_PATH, "w") as file:
                     json.dump(new_user, file, indent=4)
              
def register_users(username, password, role):
        users = load_user()

        if users:
            max_id = max(p.get("id", 0) for p in users)
            new_id = max_id + 1
        else:
            new_id = 1

        hashed_pw = hash_password(password)

        new_user = {
               "id": new_id,
               "username" : username,
               "password": hashed_pw,
               "role" : role
        }

        try:
                validate(instance=new_user, schema=schema)
        except ValidationError as e:
                print(f"Invalid user data: {e.message}")
                return

        users.append(new_user)
        add_users(users)
        print("User added successfuly!")


def login_user(username, password):
        global current_user
        users = load_user()
        for user in users:
                    if user['username'] == username:
                            if verify_password(password, user["password"]):
                                    current_user = user
                                    print(f"Logged in as {username} ({user['role']})")
                                    return True
                            else:
                                    print("Incorrect password!")
                                    return False
                            
        
        print("Username not found!")
        return False
                
def logout_user():
        global current_user
        if current_user:
                print(f"User {current_user['username']} logged out")
                current_user = None
        else:
                print("No user is currently logged in")
        
        