#!/usr/bin/python3
"""Defines the User class."""
from os import getenv
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """Represent a User."""

    if getenv("HBNB_TYPE_STORAGE") == "db":
        __tablename__ = "users"
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship(
            "Place", backref="user", cascade="all, delete, delete-orphan"
        )
        reviews = relationship(
            "Review", backref="user", cascade="all, delete, delete-orphan"
        )
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        """Initialize User."""
        super().__init__(*args, **kwargs)
        if "email" not in kwargs:
            self.email = ""
        if "password" not in kwargs:
            self.password = ""
        if "first_name" not in kwargs:
            self.first_name = ""
        if "last_name" not in kwargs:
            self.last_name = ""
