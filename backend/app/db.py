from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import time

DATABASE_URL = "postgresql://postgres:postgres@postgres:5432/postgres"

# Retry logic
for i in range(10):
    try:
        engine = create_engine(DATABASE_URL)
        engine.connect()
        print("✅ Database connected")
        break
    except Exception as e:
        print("⏳ Waiting for DB...", e)
        time.sleep(2)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
