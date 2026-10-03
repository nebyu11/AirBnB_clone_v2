#!/usr/bin/python3
"""Defines the FileStorage class."""
import json
import os


class FileStorage:
    """Serializes instances to JSON file & deserializes JSON file to instances.

    Attributes:
        __file_path (str): Path to the JSON file.
        __objects (dict): Dictionary storing all objects by <class name>.id.
    """

    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """Return the dictionary __objects, optionally filtered by cls."""
        if cls is None:
            return FileStorage.__objects
        filtered = {}
        for key, obj in FileStorage.__objects.items():
            if isinstance(cls, str):
                if obj.__class__.__name__ == cls:
                    filtered[key] = obj
            else:
                if isinstance(obj, cls) or obj.__class__ == cls:
                    filtered[key] = obj
        return filtered

    def new(self, obj):
        """Set in __objects the obj with key <obj class name>.id."""
        if obj is not None:
            key = "{}.{}".format(obj.__class__.__name__, obj.id)
            FileStorage.__objects[key] = obj

    def delete(self, obj=None):
        """Delete obj from __objects if it's inside."""
        if obj is not None:
            key = "{}.{}".format(obj.__class__.__name__, obj.id)
            if key in FileStorage.__objects:
                del FileStorage.__objects[key]

    def save(self):
        """Serialize __objects to the JSON file (path: __file_path)."""
        obj_dict = {}
        for key, obj in FileStorage.__objects.items():
            obj_dict[key] = obj.to_dict()
        with open(FileStorage.__file_path, "w", encoding="utf-8") as f:
            json.dump(obj_dict, f)

    def reload(self):
        """Deserialize the JSON file to __objects (only if file exists)."""
        if not os.path.isfile(FileStorage.__file_path):
            return
        try:
            with open(FileStorage.__file_path, "r", encoding="utf-8") as f:
                obj_dict = json.load(f)
            from models.base_model import BaseModel
            from models.user import User
            from models.state import State
            from models.city import City
            from models.amenity import Amenity
            from models.place import Place
            from models.review import Review

            classes = {
                "BaseModel": BaseModel,
                "User": User,
                "State": State,
                "City": City,
                "Amenity": Amenity,
                "Place": Place,
                "Review": Review,
            }
            for key, val in obj_dict.items():
                cls_name = val.get("__class__")
                if cls_name in classes:
                    FileStorage.__objects[key] = classes[cls_name](**val)
        except Exception:
            pass

    def close(self):
        """Call reload() method for deserializing the JSON file to objects."""
        self.reload()
