import hashlib

from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """User here...hellooo"""

    if models.storage_t == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False, unique=True)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user")
        reviews = relationship("Review", backref="user")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        """initializes user"""
        if "password" in kwargs:
            # Hash password before storing
            kwargs["password"] = hashlib.md5(kwargs["password"].encode()).hexdigest()
        super().__init__(*args, **kwargs)

    def to_dict(self, only_for_file_storage=False):
        """
        Returns a dictionary representation of the User instance.
        Excludes password by default. until you request it.
        """
        user_dict = super().to_dict(only_for_file_storage=only_for_file_storage)
        if not only_for_file_storage:
            del user_dict["password"]
        return user_dict
