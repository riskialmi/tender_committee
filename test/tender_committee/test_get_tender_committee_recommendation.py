from typing import List
from pydantic import parse_obj_as

from app.api.schemas import tender_committee as schemas
from test.tender_committee.tender_committee_attr_value import tender_committee_request

prefix = '/TenderCommittee'


def test_get_data(client, populate_data_tender_committee_request):
    response = client.get(prefix + '/TenderCommitteeRecommendation/'
                          + populate_data_tender_committee_request.request_no)

    tcr_obj_json = parse_obj_as(List[schemas.TenderCommitteeRecommendation], response.json())
    expected = parse_obj_as(List[schemas.TenderCommitteeRecommendation], tender_committee_request['recommendation'])

    assert response.status_code == 200
    assert tcr_obj_json == expected


def test_wrong_request_no(client):
    requests_no = 'TC-20220713'
    response = client.get(prefix + '/TenderCommitteeRecommendation/' + requests_no)

    assert response.status_code == 404
    assert response.json() == {'detail': f"Data not found with request number {requests_no}"}
