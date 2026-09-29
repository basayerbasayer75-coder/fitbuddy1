import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
load_dotenv()
BASE_DIR=Path(__file__).resolve().parent.parent
DATABASE_URL=os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR / 'fitbuddy.db'}")
engine=create_engine(DATABASE_URL, connect_args={"check_same_thread":False} if DATABASE_URL.startswith("sqlite") else {}, future=True)
SessionLocal=sessionmaker(bind=engine, autoflush=False, autocommit=False)
class Base(DeclarativeBase): pass
def get_db():
    db=SessionLocal()
    try: yield db
    finally: db.close()
def init_db():
    from . import models # noqa
    Base.metadata.create_all(bind=engine)
