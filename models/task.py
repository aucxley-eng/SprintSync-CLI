import uuid

class Task:
    VALID_STATUSES = ["Todo", "In Progress", "Done"]

    def __init__(self, title, assigned_to, status="Todo", task_id=None):
        self.task_id = task_id or str(uuid.uuid4())[:8]
        self.title = title
        self.assigned_to = assigned_to # User ID
        self.__status = status if status in self.VALID_STATUSES else "Todo"

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, new_status):
        """Validation logic for status updates"""
        if new_status in self.VALID_STATUSES:
            self.__status = new_status
        else:
            print(f"Error: Status must be one of {self.VALID_STATUSES}")

    def to_dict(self):
        return {
            "task_id": self.task_id,
            "title": self.title,
            "assigned_to": self.assigned_to,
            "status": self.__status
        }

    def __repr__(self):
        return f"Task({self.title} - {self.__status})"