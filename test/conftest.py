import pytest
from fastapi.testclient import TestClient

from app.auth.oauth2 import get_current_user, fake_auth_user, Session
from app.db.database import create_engine, get_db
from app.system.main import app
from app.db.models.tender_committee import Base
from test.tender_committee.tender_committee_attr_value import *


SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"


@pytest.fixture(scope="session")
def db_engine():
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    yield engine


@pytest.fixture(scope="function")
def db(db_engine):
    connection = db_engine.connect()
    connection.begin()
    # bind an individual Session to the connection
    db = Session(bind=connection)

    yield db

    db.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(db):
    app.dependency_overrides[get_db] = lambda: db
    app.dependency_overrides[get_current_user] = fake_auth_user
    with TestClient(app) as c:
        yield c

@pytest.fixture
def populate_data_tender_committee_request(db):
    return populate_tender_committee_request(db)

@pytest.fixture
def populate_data_tender_committee(db):
    return populate_tender_committee(db)

@pytest.fixture
def data_tender_committee_request(db):
    return get_tender_committee_request(db)

def clear_all_fields_in_dict(data):
    for i in data:
        data[i] = None
    return data
