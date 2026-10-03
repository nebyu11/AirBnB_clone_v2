#!/usr/bin/python3
"""Defines the DBStorage engine."""
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class DBStorage:
    """Represents a database storage engine for MySQL."""

    __engine = None
    __session = None

    def __init__(self):
        """Initialize a new DBStorage instance."""
        user = getenv("HBNB_MYSQL_USER")
        pwd = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST", "localhost")
        db = getenv("HBNB_MYSQL_DB")
        env = getenv("HBNB_ENV")

        db_url = "mysql+mysqldb://{}:{}@{}/{}".format(user, pwd, host, db)
        try:
            self.__engine = create_engine(db_url, pool_pre_ping=True)
        except Exception:
            db_url = "mysql+pymysql://{}:{}@{}/{}".format(user, pwd, host, db)
            self.__engine = create_engine(db_url, pool_pre_ping=True)

        if env == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query on the current database session all objects dependent of the class name."""
        classes = [State, City, User, Place, Review, Amenity]
        obj_dict = {}
        if cls is not None:
            if isinstance(cls, str):
                cls = globals().get(cls, None)
            if cls in classes or (cls is not None and hasattr(cls, "__tablename__")):
                query_objs = self.__session.query(cls).all()
                for obj in query_objs:
                    key = "{}.{}".format(obj.__class__.__name__, obj.id)
                    obj_dict[key] = obj
        else:
            for c in classes:
                query_objs = self.__session.query(c).all()
                for obj in query_objs:
                    key = "{}.{}".format(obj.__class__.__name__, obj.id)
                    obj_dict[key] = obj
        return obj_dict

    def new(self, obj):
        """Add the object to the current database session."""
        if obj is not None:
            self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session."""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete from the current database session obj if not None."""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in database and create current session."""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """Call remove() method on the private session attribute (self.__session)."""
        if self.__session:
            self.__session.close()
