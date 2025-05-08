# app/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# For now, use SQLite (you can change this to PostgreSQL later)
DATABASE_URL = "sqlite:///./highspell.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
