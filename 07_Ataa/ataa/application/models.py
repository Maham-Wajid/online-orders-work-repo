"""
SQLAlchemy database object and DB-related utilities.
"""
from sqlalchemy import (
    Column,
    Float,
    String,
    Integer,
    ForeignKey,
    FLOAT
)
from . import Base
from flask_login import UserMixin


class User(UserMixin, Base):
    """
    A class for user table
    """
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    email = Column(String(255))
    password = Column(String(200))
    balance = Column(FLOAT(5))
    updated_at = Column(String(20))
    created_at = Column(String(20))

    def __init__(self, name=None, email=None, password=None, balance=0, created_at=None, updated_at=None):
        self.name = name
        self.email = email
        self.password = password
        self.balance = balance
        self.created_at = created_at
        self.updated_at = updated_at


class DonationPost(Base):
    """
    A class for donation_post table
    """
    __tablename__ = 'donation_post'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    title = Column(String(255))
    description = Column(String(1500))
    requested_amount = Column(FLOAT(5))
    collected_amount = Column(FLOAT(5))
    category = Column(Integer)
    image_path = Column(String(100))
    created_at = Column(String(20))
    updated_at = Column(String(20))

    def __init__(self, user_id, title, requested_amount, collected_amount, category, image_path, description, created_at, updated_at):
        self.user_id = user_id
        self.title = title
        self.description = description
        self.requested_amount = requested_amount
        self.collected_amount = collected_amount
        self.category = category
        self.image_path = image_path
        self.created_at = created_at
        self.updated_at = updated_at


class Budget(Base):
    """
    A class for budget table
    """
    __tablename__ = 'budget'

    id = Column(Integer, primary_key=True)
    amount = Column(Integer)
    created_at = Column(String(20))
    updated_at = Column(String(20))

    def __init__(self, amount, created_at, updated_at):
        self.amount = amount
        self.created_at = created_at
        self.updated_at = updated_at
