from copy import copy

from test.conftest import clear_all_fields_in_dict
from test.tender_committee.tender_committee_attr_value import tender_committee_request
from app.api.crud.utils import random_alphanumeric
from app.api.schemas import tender_committee as schemas
from app.api.schemas.utils import ReturnSuccess
from app.api.router.utils import response_success
from app.api.crud.tender_committee import get_tender_committee_request_by_request_no, \
    get_tender_committee_recommendation_by_request_no

prefix = '/TenderCommittee'


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

def get_data_tender_committee_request(request_no, db):
    data_request = get_tender_committee_request_by_request_no(request_no, db).__dict__
    data_request['recommendation'] = get_tender_committee_recommendation_by_request_no(request_no, db)

    return schemas.FormRequest(**data_request)



def test_fill_all_fields(client, db):
    response = client.post(prefix + '/TenderCommitteeRequest/', json=tender_committee_request)

    expected_response = response_success(data=response.json()['data'])
    expected = ReturnSuccess(**expected_response)

    response_obj = ReturnSuccess(**response.json())
    data_sent = schemas.FormRequest(**tender_committee_request)
    data_saved = get_data_tender_committee_request(response.json()['data']['request_no'], db)

    assert response.status_code == 200
    assert response_obj == expected
    assert data_sent == data_saved

def test_optional_fields(client, db):
    data = copy(tender_committee_request)
    data['recommendation'][0]['directorate'] = None
    data['recommendation'][0]['division'] = None

    response = client.post(prefix + '/TenderCommitteeRequest/', json=data)

    expected_response = response_success(data=response.json()['data'])
    expected = ReturnSuccess(**expected_response)

    response_obj = ReturnSuccess(**response.json())
    data_sent = schemas.FormRequest(**data)
    data_saved = get_data_tender_committee_request(response.json()['data']['request_no'], db)

    assert response.status_code == 200
    assert response_obj == expected
    assert data_sent == data_saved


def test_must_have_at_least_one_recommendation(client):
    data = copy(tender_committee_request)
    data['recommendation'] = None

    response = client.post(prefix + '/TenderCommitteeRequest/', json=data)

    assert response.status_code == 422
    assert response.json() == response_negative_case_must_have_at_least_1_recommendation


def test_max_length_and_data_type(client):
    data = copy(tender_committee_request)
    data['agns_number'] = random_alphanumeric(size=21)
    data['memo_to'] = random_alphanumeric(size=13)
    data['subject'] = random_alphanumeric(size=101)
    data['effective_start_date'] = 'qwerty'
    data['effective_end_date'] = 'qwerty'
    data['recommendation'] = [{
        'account_name': random_alphanumeric(size=13),
        'name': random_alphanumeric(size=51),
        'email': random_alphanumeric(size=51),
        'directorate': random_alphanumeric(size=6),
        'division': random_alphanumeric(size=11),
    }]

    response = client.post(prefix + '/TenderCommitteeRequest/', json=data)

    assert response.status_code == 422
    assert response.json() == response_negative_case_max_length_and_data_type


def test_required_fields(client):
    data_tcr = clear_all_fields_in_dict(data=copy(tender_committee_request))
    data_tcr['recommendation'] = [{
        'account_name': None,
        'name': None,
        'email': None,
        'directorate': None,
        'division': None
    }]

    response = client.post(prefix + '/TenderCommitteeRequest/', json=data_tcr)

    assert response.status_code == 422
    assert response.json() == response_negative_case_required_fields
