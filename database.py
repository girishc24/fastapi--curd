from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

URL_DATABASE = 'postgresql://postgres:123123@localhost:5432/fapi'

engine = create_engine(URL_DATABASE)

SessionLocal = sessionmaker(autocommet=False, autoflush=False, bind=engine)

Base = declarative_base()