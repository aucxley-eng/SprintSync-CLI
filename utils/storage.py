#First by importing a JSON package used to work with json data
import json
import os
from jsonschema import validate, ValidationError

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
FILE_PATH = os.path.join(DATA_DIR, "projects.json")

#Generated a structure for validating the input details of project
schema = {
  "type": "array",
  "items": {
    "type": "object",
    "required": ["name", "description"],
    "properties": {
      "name": { "type": "string" },
      "description": { "type": "string" }
    }
  }
}

class JSONManager:
    
    @staticmethod
    def load_projects():
        try:
            with open(FILE_PATH, "r") as file:
                data = json.load(file)
                return data
    #Exception for when the file is not found in the directory
        except FileNotFoundError:
            print(f'Error:No such file as : {FILE_PATH}')
            return []
    #Exception for when no persmission to read file 
        except PermissionError:
            print(f'Error :No permission to read file')
            return []
    #EXception for an invalid JSON file
        except json.JSONDecodeError as e:
            print(f'Error : Invalid JSON in file - {e}')
            return []

    @staticmethod  #used to define a method that doesnt depend on class
    def save_projects(data):
        try:
            #validated the input
            validate(instance=data, schema=schema)

            #save to JSON file
            with open(FILE_PATH, 'w') as file:
                #dump is used to save data to the json file
                json.dump(data, file, indent=4)
                print('Project saved!')

        except ValidationError as e:
            print(f"Invalid data: {e}")


    @staticmethod
    def add_project(name, description,status,owner,time):
        projects = JSONManager.load_projects()

        #auto increment id
        if projects:
            max_id = max(p.get("id", 0) for p in projects)
            new_id = max_id + 1
        else:
            new_id = 1
            
        project = {
            "id" : new_id,
            "name" : name,
            "description" : description,
            "status": status,
            "owner" : owner,
            "time_created" : time
        }
        projects.append(project)
        JSONManager.save_projects(projects)
        print(f"Project '{name}' saved successfully!")