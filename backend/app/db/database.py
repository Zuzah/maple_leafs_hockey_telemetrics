from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Use environment variable set by Docker or fallback for local dev
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://telemetry:telemetry@localhost:5432/telemetry_db"
)

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
