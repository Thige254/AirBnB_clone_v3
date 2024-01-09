#!/usr/bin/python3
"""Database storage engine using SQLAlchemy with a mysql+mysqldb database
connection.
"""

import os
from models.base_model import Base
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.state import State
from models.review import Review
from models.user import User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


class DBStorage:
    """Database Storage"""
    __engine = None
    __session = None
    name2class = {
        'Amenity': Amenity,
        'City': City,
        'Place': Place,
        'State': State,
        'Review': Review,
        'User': User
    }

    def __init__(self):
        """Initializes the object"""
        user = os.getenv('HBNB_MYSQL_USER')
        passwd = os.getenv('HBNB_MYSQL_PWD')
        host = os.getenv('HBNB_MYSQL_HOST')
        database = os.getenv('HBNB_MYSQL_DB')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(user, passwd, host, database))
        if os.getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def initialize_session(self):
        """Initialize the database session"""
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(session_factory)

    def all(self, cls=None):
        """Returns a dictionary of all the objects present"""
        if not self.__session:
            self.initialize_session()
        objects = {}
        if cls and isinstance(cls, str):
            cls = self.name2class.get(cls, None)
        if cls:
            objects = {obj.__class__.__name__ + '.' + obj.id: obj
                       for obj in self.__session.query(cls)}
        else:
            for cls in self.name2class.values():
                objects.update({obj.__class__.__name__ + '.' + obj.id: obj
                                for obj in self.__session.query(cls)})
        return objects

    def new(self, obj):
        """Creates a new object"""
        self.__session.add(obj)

    def save(self):
        """Saves the current session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes an object"""
        if not self.__session:
            self.initialize_session()
        if obj:
            self.__session.delete(obj)

    def close(self):
        """Dispose of the current session if active"""
        self.__session.remove()

    def get(self, cls, id):
        """Retrieve an object"""
        if isinstance(cls, str) and cls in self.name2class and isinstance(id, str):
            cls = self.name2class[cls]
            result = self.__session.query(cls).filter(cls.id == id).first()
            return result
        else:
            return None

    def count(self, cls=None):
        """Count the number of objects in storage"""
        total = 0
        if isinstance(cls, str) and cls in self.name2class:
            cls = self.name2class[cls]
            total = self.__session.query(cls).count()
        elif cls is None:
            for cls in self.name2class.values():
                total += self.__session.query(cls).count()
        return total
