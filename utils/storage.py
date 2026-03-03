import json
import os
from typing import Any, Dict, List
from jsonschema import validate, ValidationError

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
PROJECT_FILE = os.path.join(DATA_DIR, "projects.json")

<<<<<<< HEAD
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
=======
#Generated a structure for validating the input details of project
schema: Dict[str, Any] = {
  "type": "array",
  "items": {
    "type": "object",
    "required": ["name", "description", "owner"],
    "properties": {
      "name": { "type": "string" },
      "description": { "type": "string" },
      "owner": {"type": "string"}
>>>>>>> development
    }
}

class JSONManager:

    @staticmethod
    def load_projects() -> List[Dict[str, Any]]:
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

<<<<<<< HEAD
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
        new_id = max([p.get("id", 0) for p in projects], default=0) + 1
        project = {
            "id": new_id,
            "name": name,
            "description": description,
=======
    @staticmethod  #used to define a method that doesnt depend on class
    def save_projects(data: List[Dict[str, Any]]) -> None:
        try:
            #validated the input
            validate(instance=data, schema=schema)

            #save to JSON file
            with open(FILE_PATH, 'w') as file:
                #dump is used to save data to the json file
                json.dump(data, file, indent=4)

        except ValidationError as e:
            print(f"Invalid data: {e.message}")


    @staticmethod
    def add_project(name: str, description: str, status: str, owner: str, time: str) -> None:
        projects = JSONManager.load_projects()

        #auto increment id
        if projects:
            max_id = max(p.get("id", 0) for p in projects)
            new_id = max_id + 1
        else:
            new_id = 1
            
        project: Dict[str, Any] = {
            "id" : new_id,
            "name" : name,
            "description" : description,
>>>>>>> development
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