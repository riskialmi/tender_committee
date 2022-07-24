import pytest
from fastapi.testclient import TestClient

from app.auth.oauth2 import get_current_user, fake_auth_user
from app.db.database import SessionLocal
from app.system.main import app
from test.tender_committee.tender_committee_attr_value import populate_data_module_tender_committee

clean_table = ['tender_committee', 'tender_committee_request']

def clear_all_fields_in_dict(data):
    for i in data:
        data[i] = None
    return data


@pytest.fixture(scope="module")
def client():
    app.dependency_overrides[get_current_user] = fake_auth_user
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="module")
def populate_data_test():
    db = SessionLocal()
    db.execute('TRUNCATE {} RESTART IDENTITY CASCADE;'.format(','.join(table for table in clean_table)))
    populate_data_module_tender_committee(db)

    db.commit()
    db.close()
