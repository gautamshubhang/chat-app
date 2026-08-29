import pytest
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, URL, event, text
from app.database import DatabaseSettings, Base
from alembic import command
from alembic.config import Config

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


@pytest.fixture(scope="session")
def test_database():

    config = Config("alembic.ini")

    config.set_main_option(
        "sqlalchemy.url",
        db_url.render_as_string(hide_password=False)
    )

    with test_engine.begin() as connection:
        connection.execute(text("DROP TABLE IF EXISTS alembic_version;"))

    command.upgrade(config, "head")

    yield

    # Teardown: drop all tables created during tests to wipe the test dataset
    Base.metadata.drop_all(bind=test_engine)
    test_engine.dispose()

@pytest.fixture()
def db(test_database):

    connection = test_engine.connect()
    transaction = connection.begin()

    db = TestSessionLocal(bind=connection)
    db.begin_nested()

    @event.listens_for(db, "after_transaction_end")
    def restart_savepoint(db,transaction):
        if transaction.nested and not transaction._parent.nested:
            db.begin_nested()

    try:
        yield db
    finally:
        db.rollback()
        db.close()
        connection.close()

