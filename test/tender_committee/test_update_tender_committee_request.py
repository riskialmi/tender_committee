import datetime

from app.api.crud.utils import random_alphanumeric
from test.tender_committee.tender_committee_attr_value import  tender_committee_request
from app.api.schemas import tender_committee as schemas
from app.api.router.tender_committee import response_success
from test.tender_committee.test_create_tender_committee_request import get_data_tender_committee_request

prefix = '/TenderCommittee'
now = datetime.datetime.now()

tender_committee_request_updated = {
    "agns_number": "S.0001/VIII/IIF/2021",
    "memo_to": "accounttest2",
    "subject": "subject 2",
    "effective_start_date": now.isoformat(),
    "effective_end_date": (now + datetime.timedelta(days=1)).isoformat(),
    "letter": "letter 2",
    "recommendation": [
        {
            "id": 1,
            "account_name": "accounttest3",
            "name": "account_test3",
            "email": "accounttest3@gmail.com",
            "directorate": "CIO3",
            "division": "BD3"
        },
        {
            "id": 2,
            "account_name": "accounttest4",
            "name": "account_test4",
            "email": "accounttest4@gmail.com",
            "directorate": "CIO4",
            "division": "BD4"
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



def test_update_all_fields(client, db, populate_data_tender_committee_request):
    response = client.patch(prefix + '/TenderCommitteeRequest/' + populate_data_tender_committee_request.request_no,
                            json=tender_committee_request_updated)

    data_sent = schemas.FormRequest(**tender_committee_request_updated)
    data_saved = get_data_tender_committee_request(populate_data_tender_committee_request.request_no, db)
    expected = response_success(data={'request_no': populate_data_tender_committee_request.request_no})

    assert response.status_code == 200
    assert response.json() == expected
    assert data_sent == data_saved


def test_partial_update(client, db, populate_data_tender_committee_request):
    partial_update = {
        "memo_to": "account_test",
        "subject": "subject",
        "effective_start_date": now.isoformat(),
        "effective_end_date": (now + datetime.timedelta(days=1)).isoformat(),
        "letter": "letter",
    }

    response = client.patch(prefix + '/TenderCommitteeRequest/' + populate_data_tender_committee_request.request_no,
                            json=partial_update)

    tender_committee_request.update(partial_update)
    data_sent = schemas.FormRequest(**tender_committee_request)
    data_saved = get_data_tender_committee_request(populate_data_tender_committee_request.request_no, db)
    expected = response_success(data={'request_no': populate_data_tender_committee_request.request_no})


    assert response.status_code == 200
    assert response.json() == expected
    assert  data_sent == data_saved

# def test_update_with_wrong_request_no(client):
#     request_no = 'TC-000001'
#     response = client.patch(prefix + '/TenderCommitteeRequest/Update/' + request_no,
#                             json=tender_committee_request_updated)
#
#     expected_response = {'detail': f"request number {request_no} doesn't exist"}
#
#     assert response.status_code == 404
#     assert response.json() == expected_response
#
# def test_max_length_and_data_type(client):
#     tender_committee_request['agns_number'] = random_alphanumeric(size=21)
#     tender_committee_request['memo_to'] = random_alphanumeric(size=13)
#     tender_committee_request['subject'] = random_alphanumeric(size=101)
#     tender_committee_request['effective_start_date'] = 'qwerty'
#     tender_committee_request['effective_end_date'] = 'qwerty'
#     tender_committee_request['recommendation'] = [{
#         "id": 1,
#         'account_name': random_alphanumeric(size=13),
#         'name': random_alphanumeric(size=51),
#         'email': random_alphanumeric(size=51),
#         'directorate': random_alphanumeric(size=6),
#         'division': random_alphanumeric(size=11),
#     }]
#
#     tender_committee_request_obj = populated_data(tender_committee_request_updated['agns_number'])
#     response = client.patch(prefix + '/TenderCommitteeRequest/Update/' + tender_committee_request_obj.request_no,
#                             json=tender_committee_request)
#
#     assert response.status_code == 422
#     assert response.json() == response_negative_case_max_length_and_data_type
