import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import create_engine, URL
import urllib.parse

class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    db_user: str
    db_password: str
    db_host: str
    db_port: int
    db_name: str

db_settings = DatabaseSettings()

safe_password = urllib.parse.quote_plus(db_settings.db_password)

print(f"--> APP TRYING USER: '{db_settings.db_user}'")
print(f"--> APP TRYING PASS: '{db_settings.db_password}'") 

db_url = URL.create(
    drivername="postgresql",
    username=db_settings.db_user,
    password=safe_password, 
    host=db_settings.db_host,
    port=db_settings.db_port,
    database=db_settings.db_name
)

engine = create_engine(db_url, echo=True)
session = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()
