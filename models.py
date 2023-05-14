from sqlalchemy import Column, Integer, String, Date, Float

from database import Base

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    belongs_to_collection = Column(String)
    budget = Column(Integer)
    popularity = Column(Float)
    poster_path = Column(String)
    release_date = Column(Date)
    revenue = Column(Integer)
    title = Column(String, unique=True)
    vote_average = Column(Float)
    returns = Column(Integer)
    production_companies = Column(String)
    production_countries = Column(String)
    description = Column(String)
 