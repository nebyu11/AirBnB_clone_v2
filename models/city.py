#!/usr/bin/python3
"""Defines the City class."""
from os import getenv
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class City(BaseModel, Base):
    """Represent a City."""

    if getenv("HBNB_TYPE_STORAGE") == "db":
        __tablename__ = "cities"
        name = Column(String(128), nullable=False)
        state_id = Column(String(60), ForeignKey("states.id"), nullable=False)
        places = relationship(
            "Place", backref="cities", cascade="all, delete, delete-orphan"
        )
    else:
        state_id = ""
        name = ""

    def __init__(self, *args, **kwargs):
        """Initialize City."""
        super().__init__(*args, **kwargs)
        if "name" not in kwargs:
            self.name = ""
        if "state_id" not in kwargs:
            self.state_id = ""
