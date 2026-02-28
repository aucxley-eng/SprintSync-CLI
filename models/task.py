import uuid

class Task:
    VALID_STATUSES = ["Todo", "In Progress", "Done"]

    def __init__(self, title: str, assigned_to: str, status: str = "Todo"):
        self.task_id = str(uuid.uuid4())[:8]
        self.title = title
        self.assigned_to = assigned_to
        self.__status = status if status in self.VALID_STATUSES else "Todo"

    @property
    def status(self):
        return self.__status

    def mark_as_completed(self):
        self.__status = "Done"