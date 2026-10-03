#!/usr/bin/python3
"""Defines the Place class."""
from os import getenv
import models
from models.base_model import BaseModel, Base
from models.review import Review
from models.amenity import Amenity
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship

if getenv("HBNB_TYPE_STORAGE") == "db":
    place_amenity = Table(
        "place_amenity",
        Base.metadata,
        Column(
            "place_id",
            String(60),
            ForeignKey("places.id"),
            primary_key=True,
            nullable=False
        ),
        Column(
            "amenity_id",
            String(60),
            ForeignKey("amenities.id"),
            primary_key=True,
            nullable=False
        )
    )


class Place(BaseModel, Base):
    """Represent a Place."""

    if getenv("HBNB_TYPE_STORAGE") == "db":
        __tablename__ = "places"
        city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
        user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        reviews = relationship(
            "Review", backref="place", cascade="all, delete, delete-orphan"
        )
        amenities = relationship(
            "Amenity",
            secondary=place_amenity,
            viewonly=False,
            back_populates="place_amenities"
        )
    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

        @property
        def reviews(self):
            """Get a list of all related Review objects for FileStorage."""
            review_list = []
            for review in models.storage.all(Review).values():
                if review.place_id == self.id:
                    review_list.append(review)
            return review_list

        @property
        def amenities(self):
            """Get a list of linked Amenity objects for FileStorage."""
            amenity_list = []
            for amenity in models.storage.all(Amenity).values():
                if amenity.id in self.amenity_ids:
                    amenity_list.append(amenity)
            return amenity_list

        @amenities.setter
        def amenities(self, obj):
            """Append an Amenity object id to amenity_ids."""
            if isinstance(obj, Amenity) and obj.id not in self.amenity_ids:
                self.amenity_ids.append(obj.id)

    def __init__(self, *args, **kwargs):
        """Initialize Place."""
        super().__init__(*args, **kwargs)
        if "city_id" not in kwargs:
            self.city_id = ""
        if "user_id" not in kwargs:
            self.user_id = ""
        if "name" not in kwargs:
            self.name = ""
        if "description" not in kwargs:
            self.description = ""
        if "number_rooms" not in kwargs:
            self.number_rooms = 0
        if "number_bathrooms" not in kwargs:
            self.number_bathrooms = 0
        if "max_guest" not in kwargs:
            self.max_guest = 0
        if "price_by_night" not in kwargs:
            self.price_by_night = 0
        if "latitude" not in kwargs:
            self.latitude = 0.0
        if "longitude" not in kwargs:
            self.longitude = 0.0
