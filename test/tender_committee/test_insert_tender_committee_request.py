import datetime
from pydantic import parse_obj_as

from test.conftest import clear_all_fields_in_dict
from test.tender_committee.tender_committee_attr_value import return_success, tender_committee_request as tcr
from app.api.crud.tender_committee import get_tender_committee_request_by_request_no, \
    get_tender_committee_recommendation_by_request_no
from app.api.crud.utils import random_alphanumeric
from app.api.schemas.tender_committee import FormRequest, TenderCommitteeRequest
from app.api.schemas.utils import ReturnSuccess
from app.db.database import SessionLocal

prefix = '/TenderCommittee'
now = datetime.datetime.now()
db = SessionLocal()

tender_committee_request = {}
tender_committee_request.update(tcr)
tender_committee_request['agns_number'] = 'S.9999/VIII/IIF/2021'

response_negative_case_required_fields = {
    "detail": [
        {
            "loc": [
                "body",
                "agns_number"
            ],
            "msg": "none is not an allowed value",
            "type": "type_error.none.not_allowed"
        },
        {
            "loc": [
                "body",
                "memo_to"
            ],
            "msg": "none is not an allowed value",
            "type": "type_error.none.not_allowed"
        },
        {
            "loc": [
                "body",
                "subject"
            ],
            "msg": "none is not an allowed value",
            "type": "type_error.none.not_allowed"
        },
        {
            "loc": [
                "body",
                "effective_start_date"
            ],
            "msg": "none is not an allowed value",
            "type": "type_error.none.not_allowed"
        },
        {
            "loc": [
                "body",
                "effective_end_date"
            ],
            "msg": "none is not an allowed value",
            "type": "type_error.none.not_allowed"
        },
        {
            "loc": [
                "body",
                "letter"
            ],
            "msg": "none is not an allowed value",
            "type": "type_error.none.not_allowed"
        },
        {
            "loc": [
                "body",
                "recommendation",
                0,
                "account_name"
            ],
            "msg": "none is not an allowed value",
            "type": "type_error.none.not_allowed"
        },
        {
            "loc": [
                "body",
                "recommendation",
                0,
                "name"
            ],
            "msg": "none is not an allowed value",
            "type": "type_error.none.not_allowed"
        },
        {
            "loc": [
                "body",
                "recommendation",
                0,
                "email"
            ],
            "msg": "none is not an allowed value",
            "type": "type_error.none.not_allowed"
        }
    ]
}

response_negative_case_must_have_at_least_1_recommendation = {
    "detail": [
        {
            "loc": [
                "body",
                "recommendation"
            ],
            "msg": "none is not an allowed value",
            "type": "type_error.none.not_allowed"
        }
    ]
}

response_negative_case_max_length_and_data_type = {
    "detail": [
        {
            "loc": [
                "body",
                "agns_number"
            ],
            "msg": "ensure this value has at most 20 characters",
            "type": "value_error.any_str.max_length",
            "ctx": {
                "limit_value": 20
            }
        },
        {
            "loc": [
                "body",
                "memo_to"
            ],
            "msg": "ensure this value has at most 12 characters",
            "type": "value_error.any_str.max_length",
            "ctx": {
                "limit_value": 12
            }
        },
        {
            "loc": [
                "body",
                "subject"
            ],
            "msg": "ensure this value has at most 100 characters",
            "type": "value_error.any_str.max_length",
            "ctx": {
                "limit_value": 100
            }
        },
        {
            "loc": [
                "body",
                "effective_start_date"
            ],
            "msg": "invalid datetime format",
            "type": "value_error.datetime"
        },
        {
            "loc": [
                "body",
                "effective_end_date"
            ],
            "msg": "invalid datetime format",
            "type": "value_error.datetime"
        },
        {
            "loc": [
                "body",
                "recommendation",
                0,
                "account_name"
            ],
            "msg": "ensure this value has at most 12 characters",
            "type": "value_error.any_str.max_length",
            "ctx": {
                "limit_value": 12
            }
        },
        {
            "loc": [
                "body",
                "recommendation",
                0,
                "name"
            ],
            "msg": "ensure this value has at most 50 characters",
            "type": "value_error.any_str.max_length",
            "ctx": {
                "limit_value": 50
            }
        },
        {
            "loc": [
                "body",
                "recommendation",
                0,
                "email"
            ],
            "msg": "ensure this value has at most 50 characters",
            "type": "value_error.any_str.max_length",
            "ctx": {
                "limit_value": 50
            }
        },
        {
            "loc": [
                "body",
                "recommendation",
                0,
                "directorate"
            ],
            "msg": "ensure this value has at most 5 characters",
            "type": "value_error.any_str.max_length",
            "ctx": {
                "limit_value": 5
            }
        },
        {
            "loc": [
                "body",
                "recommendation",
                0,
                "division"
            ],
            "msg": "ensure this value has at most 10 characters",
            "type": "value_error.any_str.max_length",
            "ctx": {
                "limit_value": 10
            }
        }
    ]
}


def expected_data_tender_committee_request(request_no):
    tcr_object = parse_obj_as(TenderCommitteeRequest,
                              get_tender_committee_request_by_request_no(request_no=request_no, db=db))
    tcrm_object = get_tender_committee_recommendation_by_request_no(request_no=request_no, db=db)
    db.close()

    tcr_dict = tcr_object.dict()
    tcr_dict['recommendation'] = tcrm_object
    return parse_obj_as(FormRequest, tcr_dict)


def test_fill_all_fields(client):
    response = client.post(prefix + '/TenderCommitteeRequest/Insert', json=tender_committee_request)
    return_success['data'] = response.json()['data']
    request_no = response.json()['data']['request_no']

    response_obj = parse_obj_as(ReturnSuccess, response.json())
    expected_response = parse_obj_as(ReturnSuccess, return_success)
    data_entered = parse_obj_as(FormRequest, tender_committee_request)


    assert response.status_code == 200
    assert response_obj == expected_response
    assert data_entered == expected_data_tender_committee_request(request_no=request_no)


def test_optional_fields(client):
    tender_committee_request['recommendation'][0]['directorate'] = None
    tender_committee_request['recommendation'][0]['division'] = None

    response = client.post(prefix + '/TenderCommitteeRequest/Insert', json=tender_committee_request)
    return_success['data'] = response.json()['data']
    request_no = response.json()['data']['request_no']

    response_obj = parse_obj_as(ReturnSuccess, response.json())
    data_entered = parse_obj_as(FormRequest, tender_committee_request)
    expected_response = parse_obj_as(ReturnSuccess, return_success)

    assert response.status_code == 200
    assert response_obj == expected_response
    assert data_entered == expected_data_tender_committee_request(request_no=request_no)


def test_must_have_at_least_one_recommendation(client):
    tender_committee_request['recommendation'] = None

    response = client.post(prefix + '/TenderCommitteeRequest/Insert', json=tender_committee_request)

    assert response.status_code == 422
    assert response.json() == response_negative_case_must_have_at_least_1_recommendation


def test_max_length_and_data_type(client):
    tender_committee_request['agns_number'] = random_alphanumeric(size=21)
    tender_committee_request['memo_to'] = random_alphanumeric(size=13)
    tender_committee_request['subject'] = random_alphanumeric(size=101)
    tender_committee_request['effective_start_date'] = 'qwerty'
    tender_committee_request['effective_end_date'] = 'qwerty'
    tender_committee_request['recommendation'] = [{
        'account_name': random_alphanumeric(size=13),
        'name': random_alphanumeric(size=51),
        'email': random_alphanumeric(size=51),
        'directorate': random_alphanumeric(size=6),
        'division': random_alphanumeric(size=11),
    }]

    response = client.post(prefix + '/TenderCommitteeRequest/Insert', json=tender_committee_request)

    assert response.status_code == 422
    assert response.json() == response_negative_case_max_length_and_data_type


def test_required_fields(client):
    clear_all_fields_in_dict(tender_committee_request)
    tender_committee_request['recommendation'] = [{
        'account_name': None,
        'name': None,
        'email': None,
        'directorate': None,
        'division': None
    }]

    response = client.post(prefix + '/TenderCommitteeRequest/Insert', json=tender_committee_request)

    assert response.status_code == 422
    assert response.json() == response_negative_case_required_fields
