from typing import Optional, List
from pydantic import BaseModel, constr
from datetime import datetime

from app.api.schemas.utils import _AllOptionalMeta


class ListTenderCommittee(BaseModel):
    id: Optional[int] = None
    name: constr(max_length=50)
    email: str
    directorate: Optional[constr(max_length=5)] = None
    division: Optional[constr(max_length=10)] = None
    start_date: datetime
    end_date: datetime
    is_active: Optional[bool] = None

    class Config:
        orm_mode = True


class TenderCommitteeRequest(BaseModel):
    agns_number: constr(max_length=20)
    memo_to: constr(max_length=12)
    subject: constr(max_length=100)
    effective_start_date: datetime
    effective_end_date: datetime
    letter: bytes

    class Config:
        orm_mode = True


class TenderCommitteeRecommendation(BaseModel):
    account_name: constr(max_length=12)
    name: constr(max_length=50)
    email: constr(max_length=50)
    directorate: Optional[constr(max_length=5)]
    division: Optional[constr(max_length=10)]

    class Config:
        orm_mode = True

class TenderCommitteeRecommendationAll(TenderCommitteeRecommendation):
    id: int

class FormRequest(TenderCommitteeRequest):
    recommendation: List[TenderCommitteeRecommendation]

    class Config:
        orm_mode = True

class UpdateTenderCommitteeRequest(TenderCommitteeRequest, metaclass=_AllOptionalMeta):
    recommendation: List[TenderCommitteeRecommendationAll]

class UserInformation(BaseModel):
    name: constr(max_length=100)
    email: constr(max_length=50)
    directorate: Optional[constr(max_length=5)]
    division: Optional[constr(max_length=10)]

    class Config:
        orm_mode = True

class TenderCommittee(ListTenderCommittee):
    account_name: constr(max_length=12)

    class Config:
        orm_mode = True

class UpdateTenderCommittee(BaseModel):
    effective_start_date: datetime
    effective_end_date: datetime
