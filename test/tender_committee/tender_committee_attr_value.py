from typing import List
from pydantic import parse_obj_as
import datetime

from app.auth.oauth2 import fake_auth_user
from app.api.schemas import tender_committee as schemas
from app.api.crud import tender_committee as tc_crud
from app.db.models import tender_committee as models

now = datetime.datetime.today()


tender_committee = \
    [
        {
            'id': '1',
            'is_active': True,
            'account_name': 'account1',
            'name': 'account_test1',
            'email': 'account1@gmail.com',
            'directorate': 'CIO1',
            'division': 'BD1',
            'start_date': now.isoformat(),
            'end_date': (now + datetime.timedelta(days=1)).isoformat()
        },
        {
            'id': '2',
            'is_active': True,
            'account_name': 'account2',
            'name': 'account_test2',
            'email': 'account2@gmail.com',
            'directorate': 'CIO2',
            'division': 'BD2',
            'start_date': now,
            'end_date': (now + datetime.timedelta(days=2)).isoformat()
        },
        {
            'id': '3',
            'is_active': True,
            'account_name': 'account3',
            'name': 'account_test3',
            'email': 'account3@gmail.com',
            'directorate': 'CEO1',
            'division': 'IV1',
            'start_date': now.isoformat(),
            'end_date': (now + datetime.timedelta(days=3)).isoformat()
        },
        {
            'id': '4',
            'is_active': True,
            'account_name': 'account4',
            'name': 'account_test4',
            'email': 'account4@gmail.com',
            'directorate': 'CIO1',
            'division': 'BD1',
            'start_date': now.isoformat(),
            'end_date': (now + datetime.timedelta(days=4)).isoformat()
        },
        {
            'id': '5',
            'is_active': True,
            'account_name': 'account5',
            'name': 'account_test',
            'email': 'account5@gmail.com',
            'directorate': 'CIO2',
            'division': 'BD2',
            'start_date': now.isoformat(),
            'end_date': (now + datetime.timedelta(days=5)).isoformat()
        },
        {
            'id': '6',
            'is_active': True,
            'account_name': 'account6',
            'name': 'account_test',
            'email': 'account6@gmail.com',
            'directorate': 'CIO2',
            'division': 'BD2',
            'start_date': now.isoformat(),
            'end_date': (now + datetime.timedelta(days=6)).isoformat()
        },
        {
            'id': '7',
            'is_active': True,
            'account_name': 'account7',
            'name': 'account_test',
            'email': 'account7@gmail.com',
            'directorate': 'CIO1',
            'division': 'BD1',
            'start_date': now.isoformat(),
            'end_date': (now + datetime.timedelta(days=7)).isoformat()
        },
        {
            'id': '8',
            'is_active': True,
            'account_name': 'account8',
            'name': 'account_test',
            'email': 'account8@gmail.com',
            'directorate': 'CIO8',
            'division': 'BD8',
            'start_date': now.isoformat(),
            'end_date': (now + datetime.timedelta(days=8)).isoformat()
        },
        {
            'id': '9',
            'is_active': True,
            'account_name': 'account9',
            'name': 'account_test',
            'email': 'account9@gmail.com',
            'directorate': 'CIO9',
            'division': 'BD9',
            'start_date': now.isoformat(),
            'end_date': (now + datetime.timedelta(days=9)).isoformat()
        },
        {
            'id': '10',
            'is_active': True,
            'account_name': 'account10',
            'name': 'account_test',
            'email': 'account10@gmail.com',
            'directorate': 'CIO10',
            'division': 'BD10',
            'start_date': now.isoformat(),
            'end_date': (now + datetime.timedelta(days=10)).isoformat()
        },

    ]


tender_committee_request = {
    "agns_number": "S.0000/VIII/IIF/2021",
    "memo_to": "account_test",
    "subject": "subject 1",
    "effective_start_date": now.isoformat(),
    "effective_end_date": (now + datetime.timedelta(days=1)).isoformat(),
    "letter": "letter",
    "recommendation": [
        {
            "account_name": "accounttest1",
            "name": "account_test1",
            "email": "accounttest1@gmail.com",
            "directorate": "CIO1",
            "division": "BD1"
        },
        {
            "account_name": "accounttest2",
            "name": "account_test2",
            "email": "accounttest2@gmail.com",
            "directorate": "CIO2",
            "division": "BD2"
        }
    ]
}


def populate_tender_committee(db):
    tender_committee_obj = parse_obj_as(List[schemas.TenderCommittee], tender_committee)
    for data in tender_committee_obj:
        db.add(tc_crud.create_tender_committee(data))

    db.commit()
    return tender_committee_obj

def populate_tender_committee_request(db):
    tender_committee_request_obj = schemas.FormRequest(**tender_committee_request)
    return tc_crud.create_tender_committee_request(param=tender_committee_request_obj, current_user=fake_auth_user(), db=db)

def get_tender_committee_request(db):
    return db.query(models.TenderCommitteeRequest).one()
