import uuid
from datetime import datetime
from typing import Dict, List

class Project:
    def __init__(self, title: str, description: str, due_date_str: str) -> None:
        if not title or title.isspace():
            raise ValueError("Project title cannot be empty.")
        
        self.project_id: str = str(uuid.uuid4())[:8]
        self.title: str = title
        self.description: str = description
        self.members: List[str] = [] # List of user emails

        try:
            self.due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Invalid date format. Use YYYY-MM-DD.")

    # Add a user (member) to the project
    def add_member(self, user_email: str) -> bool:
        if user_email not in self.members:
            self.members.append(user_email)
            return True 
        return False

    def to_dict(self) -> Dict[str, object]:
        return {
            "project_id": self.project_id,
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date.isoformat(),
            "members": self.members
        }
