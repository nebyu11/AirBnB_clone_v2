# AirBnB Clone - The Console

This repository contains the first step towards building a full web application: the **command interpreter** (console) for the AirBnB clone project.

## Description

The console is a command-line interface that allows managing the storage engine and data objects of the AirBnB project. With the console, you can:
- Create new objects (e.g. `BaseModel`, `User`, `State`, `City`, `Amenity`, `Place`, `Review`)
- Retrieve objects from a file
- Perform operations on objects (show, destroy, update, all)
- Store objects into a JSON file (`file.json`)

## Supported Classes

- `BaseModel`: Parent class for all models
- `User`: Represents user information
- `State`: Represents a geographical state
- `City`: Represents a city within a state
- `Amenity`: Represents an amenity offered at a place
- `Place`: Represents an accommodation listing
- `Review`: Represents a review left by a user for a place

## How to Start the Console

Run `./console.py` or `python3 console.py`:

```bash
$ ./console.py
(hbnb)
```

## How to Use

### Interactive Mode

```bash
$ ./console.py
(hbnb) help

Documented commands (type help <topic>):
========================================
EOF  all  create  destroy  help  quit  show  update

(hbnb) create BaseModel
49faff9a-6318-451f-87b6-910505c55907
(hbnb) show BaseModel 49faff9a-6318-451f-87b6-910505c55907
[BaseModel] (49faff9a-6318-451f-87b6-910505c55907) {'created_at': datetime.datetime(2017, 10, 2, 3, 10, 25, 903293), 'id': '49faff9a-6318-451f-87b6-910505c55907', 'updated_at': datetime.datetime(2017, 10, 2, 3, 10, 25, 903300)}
(hbnb) update BaseModel 49faff9a-6318-451f-87b6-910505c55907 first_name "Betty"
(hbnb) destroy BaseModel 49faff9a-6318-451f-87b6-910505c55907
(hbnb) quit
$
```

### Non-Interactive Mode

```bash
$ echo "help" | ./console.py
(hbnb)

Documented commands (type help <topic>):
========================================
EOF  all  create  destroy  help  quit  show  update

(hbnb)
```

## Authors
- Yonas Leykun
- Nebyu Assefa

