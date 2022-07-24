import datetime
from pydantic import parse_obj_as

from test.tender_committee.tender_committee_attr_value import tender_committee_request
from app.api.schemas.tender_committee import TenderCommitteeRequest
from app.db.models import tender_committee as models
from app.db.database import SessionLocal

prefix = '/TenderCommittee'
now = datetime.datetime.now()
db = SessionLocal()


def expected_data_tender_committee_request(agns_number):
    tcr = models.TenderCommitteeRequest
    tcr_data = db.query(tcr.request_no,
                        tcr.agns_number,
                        tcr.memo_to,
                        tcr.subject,
                        tcr.effective_start_date,
                        tcr.effective_end_date,
                        tcr.letter,
                        tcr.status
                        ) \
        .filter(tcr.agns_number == agns_number) \
        .first()

    db.close()

    return tcr_data


def test_get_data(client):
    tender_committee_request_obj = expected_data_tender_committee_request(tender_committee_request['agns_number'])
    response = client.get(prefix + '/TenderCommitteeRequest/Get/' + tender_committee_request_obj.request_no)

    response_obj = parse_obj_as(TenderCommitteeRequest, response.json())
    expected_response = parse_obj_as(TenderCommitteeRequest, tender_committee_request_obj)

    assert response.status_code == 200
    assert response_obj == expected_response


def test_wrong_request_no(client):
    requests_no = 'TC-20220713'
    response = client.get(prefix + '/TenderCommitteeRequest/Get/' + requests_no)

    expected_response = {
        "detail": f"request number {requests_no} doesn't exist"
    }

    assert response.status_code == 404
    assert response.json() == expected_response
