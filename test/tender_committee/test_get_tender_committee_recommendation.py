import datetime
from typing import List

from pydantic import parse_obj_as

from test.tender_committee.tender_committee_attr_value import tender_committee_request
from app.api.schemas.tender_committee import TenderCommitteeRecommendation
from app.api.crud.tender_committee import get_tender_committee_recommendation_by_request_no
from app.db.database import SessionLocal
from test.tender_committee.test_get_tender_committee_request import expected_data_tender_committee_request

prefix = '/TenderCommittee'
now = datetime.datetime.now()
db = SessionLocal()

def expected_data_tender_committee_recommendation(request_no):
    data = get_tender_committee_recommendation_by_request_no(request_no=request_no, db=db)
    return parse_obj_as(List[TenderCommitteeRecommendation], data)


def test_get_data(client, populate_data_test):
    tender_committee_request_obj = expected_data_tender_committee_request(tender_committee_request['agns_number'])
    response = client.get(prefix + '/TenderCommitteeRecommendation/Get/' + tender_committee_request_obj.request_no)

    response_obj = parse_obj_as(List[TenderCommitteeRecommendation], response.json())

    assert response.status_code == 200
    assert response_obj == expected_data_tender_committee_recommendation(tender_committee_request_obj.request_no)


def test_wrong_request_no(client):
    requests_no = 'TC-20220713'
    response = client.get(prefix + '/TenderCommitteeRecommendation/Get/' + requests_no)

    assert response.status_code == 200
    assert len(response.json()) == 0
    assert response.json() == []
