#!/usr/bin/python3
"""Defines the Review class."""
from os import getenv
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey


class Review(BaseModel, Base):
    """Represent a Review."""

    if getenv("HBNB_TYPE_STORAGE") == "db":
        __tablename__ = "reviews"
        text = Column(String(1024), nullable=False)
        place_id = Column(String(60), ForeignKey("places.id"), nullable=False)
        user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    else:
        place_id = ""
        user_id = ""
        text = ""

    def __init__(self, *args, **kwargs):
        """Initialize Review."""
        super().__init__(*args, **kwargs)
        if "place_id" not in kwargs:
            self.place_id = ""
        if "user_id" not in kwargs:
            self.user_id = ""
        if "text" not in kwargs:
            self.text = ""
