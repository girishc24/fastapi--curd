from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Corrected URL for PostgreSQL
URL_DATABASE = 'postgresql://postgres:123123@localhost:5432/fapi'

# Create the database engine
engine = create_engine(URL_DATABASE)

# Correct the typo: it should be 'autocommit', not 'autocommet'
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declarative models
Base = declarative_base()
