import pytest
from typing import List
from pydantic import parse_obj_as

from app.api.schemas.tender_committee import ListTenderCommittee
from test.tender_committee.tender_committee_attr_value import tender_committee

prefix = '/TenderCommittee'

paging = {
    "sortColumn": "asc",
    "sortColumnDir": "id",
    "pageNumber": 1,
    "pageSize": 5
}


@pytest.fixture(scope="module")
def expected_data_list_tender_committee():
    return parse_obj_as(List[ListTenderCommittee], tender_committee)


def test_get_five_first_data(client, expected_data_list_tender_committee):
    response = client.post(prefix + '/ListTenderCommittee', json=paging)
    response_obj = parse_obj_as(List[ListTenderCommittee], response.json())

    assert response.status_code == 200
    assert response_obj == expected_data_list_tender_committee[:5]

def test_get_five_second_data(client, expected_data_list_tender_committee):
    paging['pageNumber'] = 2
    paging['pageSize'] = 5
    response = client.post(prefix + '/ListTenderCommittee', json=paging)
    response_obj = parse_obj_as(List[ListTenderCommittee], response.json())

    assert response.status_code == 200
    assert response_obj == expected_data_list_tender_committee[5:10]

def test_get_nothing(client):
    paging['pageNumber'] = 3
    paging['pageSize'] = 5
    response = client.post(prefix + '/ListTenderCommittee', json=paging)

    assert response.status_code == 200
    assert len(response.json()) == 0
    assert response.json() == []


