from sqlalchemy import Column, ForeignKey, Integer, String, Numeric, DateTime, Boolean
from sqlalchemy.orm import relationship
import datetime

from ssa.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    role = Column(Integer, nullable=False, default=0)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    salt = Column(String, nullable=False, default="")
    amount = Column(Numeric, nullable=False, default=0.0)
    personal_key = Column(String, nullable=False)
    salt_key = Column(String, nullable=False, default="")

    # Back population of algorithms made by this user 
    algorithms = relationship("Algorithm", back_populates="author")

    # Back population of calls made by this user
    calls = relationship("Call", back_populates="user")


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    desc = Column(String(150), nullable=True, default="")

    # Back population of algorithms in this category 
    algorithms = relationship("Algorithm", back_populates="category")


class Algorithm(Base):
    __tablename__ = "algorithms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    desc = Column(String, nullable=True, default="")
    cost = Column(Numeric, nullable=False)
    readme = Column(String, nullable=True)

    # Category the algorithm belongs to
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship("Category", back_populates="algorithms")

    # Author of the algorithm 
    author_id = Column(Integer, ForeignKey('users.id'))
    author = relationship("User", back_populates="algorithms")

    # Back population of calls madeto this algorithm
    calls = relationship("Call", back_populates="algorithm")


class Call(Base):
    __tablename__ = "calls"

    id = Column(Integer, primary_key=True, index=True)
    datetime = Column(DateTime, default=datetime.datetime.now)
    success = Column(Boolean)

    # User who used an algorithm
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="calls")

    # Algorithm used
    algorithm_id = Column(Integer, ForeignKey('algorithms.id'))
    algorithm = relationship("Algorithm", back_populates="calls")