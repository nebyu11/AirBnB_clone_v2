#!/usr/bin/python3
"""Entry point of the command interpreter for the AirBnB clone project."""
import cmd
import re
import shlex
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review

CLASSES = {
    "BaseModel": BaseModel,
    "User": User,
    "State": State,
    "City": City,
    "Amenity": Amenity,
    "Place": Place,
    "Review": Review,
}


def parse_args(arg):
    """Parse command line string into a list of arguments."""
    try:
        return shlex.split(arg)
    except Exception:
        return arg.split()


class HBNBCommand(cmd.Cmd):
    """Command interpreter for HBNB."""

    prompt = "(hbnb) "

    def emptyline(self):
        """Do nothing when an empty line is entered."""
        pass

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, arg):
        """EOF command to exit the program"""
        print()
        return True

    def do_create(self, arg):
        """Creates a new instance of a class, saves it and prints id."""
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in CLASSES:
            print("** class doesn't exist **")
        else:
            kwargs = {}
            for param in args[1:]:
                if "=" not in param:
                    continue
                key, val = param.split("=", 1)
                if not key:
                    continue
                if val.startswith('"') and val.endswith('"') and len(val) >= 2:
                    val = val[1:-1].replace('\\"', '"').replace('_', ' ')
                    kwargs[key] = val
                elif "." in val:
                    try:
                        kwargs[key] = float(val)
                    except ValueError:
                        continue
                else:
                    try:
                        kwargs[key] = int(val)
                    except ValueError:
                        continue
            new_instance = CLASSES[args[0]](**kwargs)
            new_instance.save()
            print(new_instance.id)

    def do_show(self, arg):
        """Prints string representation of instance by class name and id."""
        args = parse_args(arg)
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in CLASSES:
            print("** class doesn't exist **")
        elif len(args) < 2:
            print("** instance id missing **")
        else:
            key = "{}.{}".format(args[0], args[1])
            if key not in storage.all():
                print("** no instance found **")
            else:
                print(storage.all()[key])

    def do_destroy(self, arg):
        """Deletes instance based on class name and id & saves change."""
        args = parse_args(arg)
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in CLASSES:
            print("** class doesn't exist **")
        elif len(args) < 2:
            print("** instance id missing **")
        else:
            key = "{}.{}".format(args[0], args[1])
            if key not in storage.all():
                print("** no instance found **")
            else:
                del storage.all()[key]
                storage.save()

    def do_all(self, arg):
        """Prints string representation of all instances."""
        args = parse_args(arg)
        if len(args) > 0 and args[0] not in CLASSES:
            print("** class doesn't exist **")
        else:
            obj_list = []
            cls = CLASSES[args[0]] if len(args) > 0 else None
            for key, obj in storage.all(cls).items():
                obj_list.append(str(obj))
            print(obj_list)

    def do_count(self, arg):
        """Retrieves the number of instances of a class."""
        args = parse_args(arg)
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in CLASSES:
            print("** class doesn't exist **")
        else:
            cnt = sum(1 for k in storage.all() if k.startswith(args[0] + "."))
            print(cnt)

    def do_update(self, arg):
        """Updates an instance based on class name and id with attribute."""
        args = parse_args(arg)
        if len(args) == 0:
            print("** class name missing **")
            return
        if args[0] not in CLASSES:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        key = "{}.{}".format(args[0], args[1])
        if key not in storage.all():
            print("** no instance found **")
            return
        if len(args) < 3:
            print("** attribute name missing **")
            return
        if len(args) < 4:
            print("** value missing **")
            return

        obj = storage.all()[key]
        attr_name = args[2]
        attr_val = args[3]

        if hasattr(obj, attr_name):
            attr_type = type(getattr(obj, attr_name))
            try:
                attr_val = attr_type(attr_val)
            except (ValueError, TypeError):
                pass
        else:
            if attr_val.isdigit():
                attr_val = int(attr_val)
            else:
                try:
                    attr_val = float(attr_val)
                except ValueError:
                    pass

        setattr(obj, attr_name, attr_val)
        obj.save()

    def default(self, line):
        """Default method when input is not recognized as a command."""
        match = re.search(r"^(\w+)\.(\w+)\((.*)\)$", line)
        if not match:
            print("*** Unknown syntax: {}".format(line))
            return False
        cls_name = match.group(1)
        method = match.group(2)
        args_str = match.group(3)

        if method == "all":
            self.do_all(cls_name)
        elif method == "count":
            self.do_count(cls_name)
        elif method == "show":
            id_arg = args_str.strip('"\'')
            self.do_show("{} {}".format(cls_name, id_arg))
        elif method == "destroy":
            id_arg = args_str.strip('"\'')
            self.do_destroy("{} {}".format(cls_name, id_arg))
        elif method == "update":
            self._handle_dot_update(cls_name, args_str)
        else:
            print("*** Unknown syntax: {}".format(line))
            return False

    def _handle_dot_update(self, cls_name, args_str):
        """Helper to handle dot notation update commands."""
        if args_str.startswith("{") or ", {" in args_str:
            parts = args_str.split(", ", 1)
            if len(parts) == 2:
                id_arg = parts[0].strip('"\'')
                dict_str = parts[1]
                try:
                    import ast
                    attr_dict = ast.literal_eval(dict_str)
                    if isinstance(attr_dict, dict):
                        for k, v in attr_dict.items():
                            val_s = '"{}"'.format(v) if isinstance(
                                v, str) else str(v)
                            cmd_str = "{} {} {} {}".format(
                                cls_name, id_arg, k, val_s)
                            self.do_update(cmd_str)
                except Exception:
                    pass
        else:
            parts = [p.strip().strip('"\'') for p in args_str.split(",")]
            if len(parts) >= 3:
                val_s = '"{}"'.format(parts[2])
                cmd_str = "{} {} {} {}".format(
                    cls_name, parts[0], parts[1], val_s)
                self.do_update(cmd_str)
            elif len(parts) == 2:
                self.do_update("{} {} {}".format(
                    cls_name, parts[0], parts[1]))
            elif len(parts) == 1:
                self.do_update("{} {}".format(cls_name, parts[0]))


if __name__ == '__main__':
    HBNBCommand().cmdloop()
