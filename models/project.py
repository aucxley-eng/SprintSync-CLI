import uuid

class Project:
    def __init__(self, title, description, due_date, project_id=None):
        self.project_id = project_id or str(uuid.uuid4())[:8]
        self.title = title
        self.description = description
        self.due_date = due_date
        self.__tasks = []  # Encapsulation: Private list of tasks

    @property
    def tasks(self):
        """Getter for tasks - prevents direct overwriting of the list"""
        return self.__tasks

    def add_task(self, task_obj):
        """Associates a Task object with this project"""
        self.__tasks.append(task_obj)

    def calculate_progress(self):
        """Calculates percentage of completed tasks"""
        if not self.__tasks:
            return 0
        completed = [t for t in self.__tasks if t.status == "Done"]
        return (len(completed) / len(self.__tasks)) * 100

    def to_dict(self):
        """Converts object to dictionary for JSON storage"""
        return {
            "project_id": self.project_id,
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
            "tasks": [t.to_dict() for t in self.__tasks]
        }

    def __str__(self):
        return f"Project: {self.title} ({self.calculate_progress()}% Complete)"