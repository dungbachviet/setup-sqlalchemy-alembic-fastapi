from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  # Change this to your database URL
# engine = create_engine(SQLALCHEMY_DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


SQLALCHEMY_DATABASE_URL = "postgresql://postgres:KrrCsf5LHdvmnI7YG8@localhost:5432/test_database"  # Change this to your database URL
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# # Create tables
# Base.metadata.create_all(bind=engine)