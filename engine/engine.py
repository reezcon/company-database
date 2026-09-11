import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
port = int(os.getenv("DB_PORT", 5432))
database = os.getenv("DB_NAME")


def get_connection():
    engine_url = URL.create(
            "postgresql+psycopg2",
            username = user,
            password = password,
            host = host, 
            port = port,
            database = database,
        )
    try:
        engine = create_engine(engine_url, future=True)
    except Exception as e:
        print(f"Connection failed: {e}")
        raise SystemExit(1)
    return engine


SessionLocal = sessionmaker(bind=get_connection(), future=True)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()
