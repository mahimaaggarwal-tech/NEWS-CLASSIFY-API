from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from sqlalchemy.exc import SQLAlchemyError

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    except SQLAlchemyError as e:
        # Log or handle the error as needed
        print(f"Database error: {e}")
        db.rollback()  # Rollback any uncommitted changes in case of an error
    finally:
        db.close()
