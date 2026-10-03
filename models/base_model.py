#!/usr/bin/python3
"""Defines the BaseModel class."""
from datetime import datetime
from os import getenv
import uuid
import models
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

TIME_FMT = "%Y-%m-%dT%H:%M:%S.%f"

if getenv("HBNB_TYPE_STORAGE") == "db":
    Base = declarative_base()
else:
    Base = object


class BaseModel:
    """Defines all common attributes/methods for other classes."""

    if getenv("HBNB_TYPE_STORAGE") == "db":
        id = Column(String(60), primary_key=True, nullable=False)
        created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
        updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """Initialize a new BaseModel instance."""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

        if kwargs:
            for key, value in kwargs.items():
                if key == "__class__":
                    continue
                elif key in ("created_at", "updated_at"):
                    if isinstance(value, str):
                        setattr(self, key, datetime.strptime(value, TIME_FMT))
                    else:
                        setattr(self, key, value)
                else:
                    setattr(self, key, value)
        if not kwargs:
            if getenv("HBNB_TYPE_STORAGE") != "db":
                models.storage.new(self)

    def save(self):

        """Update updated_at with current datetime and save to storage."""
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """Return a dictionary containing all keys/values of __dict__."""
        res = self.__dict__.copy()
        res["__class__"] = self.__class__.__name__
        if isinstance(res.get("created_at"), datetime):
            res["created_at"] = res["created_at"].isoformat()
        if isinstance(res.get("updated_at"), datetime):
            res["updated_at"] = res["updated_at"].isoformat()
        res.pop("_sa_instance_state", None)
        return res

    def delete(self):
        """Delete current instance from storage."""
        models.storage.delete(self)

    def __str__(self):
        """Return string representation of the BaseModel instance."""
        d = self.__dict__.copy()
        d.pop("_sa_instance_state", None)
        return "[{}] ({}) {}".format(self.__class__.__name__, self.id, d)
