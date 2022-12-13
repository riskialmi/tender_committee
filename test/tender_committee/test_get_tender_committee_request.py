from test.tender_committee.tender_committee_attr_value import tender_committee_request
from app.api.schemas import tender_committee as schemas

prefix = '/TenderCommittee'


def test_get_data(client, populate_data_tender_committee_request):
    response = client.get(prefix + '/TenderCommitteeRequest/' + populate_data_tender_committee_request.request_no)

    response_obj = schemas.TenderCommitteeRequest(**response.json())
    expected = schemas.TenderCommitteeRequest(**tender_committee_request)

    assert response.status_code == 200
    assert response_obj == expected


def test_wrong_request_no(client):
    requests_no = 'TC-20220713'
    response = client.get(prefix + '/TenderCommitteeRequest/' + requests_no)

    expected = {
        "detail": f"Request number {requests_no} doesn't exist"
    }

    assert response.status_code == 404
    assert response.json() == expected
