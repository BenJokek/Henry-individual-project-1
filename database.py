from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

my_variable_value = os.getenv("MY_VARIABLE")

user = os.getenv("USER")
password = os.getenv("PASSWORD")
host = os.getenv("HOST")
database = os.getenv("DATABASE")

SQLALCHEMY_DATABASE_URL = f'postgresql+psycopg2://{user}:{password}@{host}/{database}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()