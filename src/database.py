from pydantic_settings import BaseSettings
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# Settings class jo .env se DATABASE_URL uthaye gi
class Settings(BaseSettings):
  DATABASE_URL: str
  DB_USER: str
  DB_PASSWORD: str
  DB_NAME: str

  class Config:
    env_file = ".env"
    extra = "ignore"


settings = Settings()

# SQLAlchemy Engine create karein
engine = create_engine(settings.DATABASE_URL)

# SessionLocal session generate karne ke liye
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class jiske zariye models banenge
Base = declarative_base()


# Dependency function jo har API route mein database session degi
def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()