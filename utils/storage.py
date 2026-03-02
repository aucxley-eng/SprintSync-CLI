import json
import os
from jsonschema import validate, ValidationError

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
PROJECT_FILE = os.path.join(DATA_DIR, "projects.json")

schema = {
    "type": "array",
    "items": {
        "type": "object",
        "required": ["id", "name", "description", "status", "owner", "time_created", "deadline", "tasks"],
        "properties": {
            "id": {"type": "number"},
            "name": {"type": "string"},
            "description": {"type": "string"},
            "status": {"type": "string"},
            "owner": {"type": "string"},
            "time_created": {"type": "string"},
            "deadline": {"type": "string"},
            "tasks": {"type": "array"}
        }
    }
}
class JSONManager:

    @staticmethod
    def load_projects():
        try:
            with open(PROJECT_FILE, "r") as f:
                data = json.load(f)
                # Ensure old projects have deadline and tasks
                for p in data:
                    if "deadline" not in p:
                        p["deadline"] = "N/A"
                    if "tasks" not in p:
                        p["tasks"] = []
                return data
        except FileNotFoundError:
            return []
        except PermissionError:
            print("[red]No permission to read file[/red]")
            return []
        except json.JSONDecodeError as e:
            print(f"[red]Invalid JSON: {e}[/red]")
            return []

    @staticmethod
    def save_projects(data):
        try:
            validate(data, schema)
            with open(PROJECT_FILE, "w") as f:
                json.dump(data, f, indent=4)
        except ValidationError as e:
            print(f"[red]Invalid project data: {e}[/red]")

    @staticmethod
    def add_project(name, description, status, owner, time, deadline):
        projects = JSONManager.load_projects()
        existing_ids = [p.get("id", 0) for p in projects]
        new_id = max(existing_ids, default=0) +1
        project = {
            "id": new_id,
            "name": name,
            "description": description,
            "status": status,
            "owner": owner,
            "time_created": time,
            "deadline": deadline,
            "tasks": []
        }
        projects.append(project)
        JSONManager.save_projects(projects)
        print(f"[green]Project '{name}' added successfully![/green]")

    @staticmethod
    def list_projects():
        return JSONManager.load_projects()
    
    @staticmethod
    def update_project(data):
        project_id = int(input('Enter project id to update : '))

        project = next((p for p in data if p["id"] == project_id), None)

        if not project:
            print("Project not found")
            return
        
        project["name"] = input("Enter a new project name :")
        project["description"] = input("Enter a new project description :")

        try:
            with open(PROJECT_FILE, "w") as file:
                json.dump(data, file, indent=4)
                print("Project updated successfuly!")
        except Exception as e:
            print(f"Error:, {e}")
            return[]

    @staticmethod
    def delete_project(data):

        project_id = int(input("Enter project id to delete :"))

        project = next((p for p in data if p["id"] == project_id), None)

        if not project:
            print("Project not found")
            return
        
        data.remove(project)

        try:
            with open(PROJECT_FILE, "w") as file:
                json.dump(data, file, indent=4)
            print("Project deleted successfully!")
        except Exception as e:
            print(f"Error: {e}")



        