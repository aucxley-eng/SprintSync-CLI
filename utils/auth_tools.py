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

# current_user is initialised after helpers are defined (see below)

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
USER_FILE = os.path.join(DATA_DIR, "users.json")
SESSION_FILE = os.path.join(DATA_DIR, "session.json")


def _load_session():
    """Load the persisted login session (if any) from disk."""
    try:
        with open(SESSION_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def _save_session(user):
    with open(SESSION_FILE, "w") as f:
        json.dump(user, f, indent=4)


def _clear_session():
    try:
        os.remove(SESSION_FILE)
    except FileNotFoundError:
        pass


current_user = _load_session()


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password: str, hashed_password: str) -> bool:
    return hash_password(password) == hashed_password


def load_users():
    try:
        with open(USER_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except PermissionError:
        print("Access denied")
        return []


def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=4)


def register_users(username, password, role):
    users = load_users()
    new_id = max([u.get("id", 0) for u in users], default=0) + 1
    hashed_pw = hash_password(password)
    new_user = {"id": new_id, "username": username, "password": hashed_pw, "role": role}

    try:
        validate(new_user, schema)
    except ValidationError as e:
        print(f"Invalid user data: {e.message}")
        return

    users.append(new_user)
    save_users(users)
    print("[green]User added successfully![/green]")


def login_user(username, password):
    global current_user
    users = load_users()
    for user in users:
        if user["username"] == username:
            if verify_password(password, user["password"]):
                current_user = user
                _save_session(user)  # persist session across invocations
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
        _clear_session()  # remove persisted session
    else:
        print("No user is currently logged in")