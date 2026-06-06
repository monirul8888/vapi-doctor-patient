import datetime as dt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

# PostgreSQL URL format:
# postgresql://username:password@host:port/dbname
DATABASE_URL = "postgresql://postgres:1234@localhost/appointments_db"


engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def init_db() -> None:
    """Create all tables in the database."""
    Base.metadata.create_all(bind=engine)


def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()