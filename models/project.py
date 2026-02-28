import uuid
from models.task import Task

class Project:
    def __init__(self, name: str, deadline: str):
        if not name:
            raise ValueError("Project name cannot be empty.")
        # TODO: validate deadline is not in the past
        self.project_id = str(uuid.uuid4())[:8]
        self.name = name
        self.deadline = deadline
        self.tasks = []

    def add_task(self, task: Task):
        self.tasks.append(task)

    def calculate_progress(self) -> float:
        if not self.tasks:
            return 0.0
        completed = sum(1 for t in self.tasks if t.status == "Done")
        return (completed / len(self.tasks)) * 100