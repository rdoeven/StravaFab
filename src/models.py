from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Column, Integer, String, ForeignKey, Float, create_engine
)

# The Base class is where all table classes inherit from
Base = declarative_base()


class Person(Base):
    __tablename__ = "person"

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    room_number = Column(Integer, nullable=False)


class Weekly(Base):
    __tablename__ = "weekly"

    # These 3 form the primary key
    runner_id = Column(Integer, ForeignKey(Person.id), primary_key=True)
    year = Column(Integer, primary_key=True)
    week = Column(Integer, primary_key=True)

    distance = Column(Float)  # Total distance run
    time = Column(Integer)  # Total time run
    velocity = Column(Float)  # Average speed throughout the week
    activity_count = Column(Integer)  # Amount of runs
    best_distance = Column(Float)  # Length of the longest run
    best_time = Column(Integer)  # Duration of the longest run


# Connect to database and create tables where needed
engine = create_engine('sqlite:///data/data.db')
Base.metadata.create_all(engine)
