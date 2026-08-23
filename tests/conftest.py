import pytest
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, URL
from app.database import DatabaseSettings, Base


db_settings = DatabaseSettings()

db_url = URL.create(
    drivername="postgresql",
    username=db_settings.db_user,
    password=db_settings.db_password, 
    host=db_settings.db_host,
    port=db_settings.db_port,
    database='family_chat_test'
)

test_engine = create_engine(db_url, echo=True)

TestSessionLocal = sessionmaker(bind=test_engine)

@pytest.fixture
def db():
    Base.metadata.create_all(bind=test_engine)

    db = TestSessionLocal()

    try:
        yield db
    finally:
        db.close()