from decouple import config
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = config("DATABASE_URL")

engine = create_engine(
    DATABASE_URL,
    future=True,
    pool_pre_ping=True,  # if connection is dead, it reconnects automatically
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
