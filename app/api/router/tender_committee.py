from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from typing import List

from app.api.router.utils import response_success
from app.api.schemas import tender_committee as schemas, utils as u_schemas
from app.api.crud import tender_committee, user_management
from app.api.schemas.user_management import UserBase
from app.auth.oauth2 import get_current_user
from app.db.database import get_db


router = APIRouter(prefix="/TenderCommittee",
                   tags=["Tender Committee"])


@router.post("/", response_model=List[schemas.ListTenderCommittee], )
async def list_tender_committee(request: u_schemas.Pagination, current_user: UserBase = Depends(get_current_user),
                          db: Session = Depends(get_db)):
    return tender_committee.get_list_active_tender_committee(request, db)


@router.get("/UserInformation/{account_name}", response_model=schemas.UserInformation, )
async def get_user_information(account_name: str, current_user: UserBase = Depends(get_current_user),
                         db: Session = Depends(get_db)):
    return user_management.get_user_information_by_account_name(account_name, db)


@router.post("/TenderCommitteeRequest/", response_model=u_schemas.ReturnSuccess)
async def create_tender_committee_request(request: schemas.FormRequest, current_user: UserBase = Depends(get_current_user),
                                    db: Session = Depends(get_db)):
    tcr = tender_committee.create_tender_committee_request(request, current_user, db)
    return response_success(data={'request_no': tcr.request_no})


@router.get("/TenderCommitteeRequest/{request_no}", response_model=schemas.TenderCommitteeRequest)
async def get_tender_committee_request(request_no: str, current_user: UserBase = Depends(get_current_user),
                                 db: Session = Depends(get_db)):
    return tender_committee.get_tender_committee_request_by_request_no(request_no, db)


@router.get("/TenderCommitteeRecommendation/{request_no}", response_model=List[schemas.TenderCommitteeRecommendationAll])
async def get_tender_committee_recommendation(request_no: str, current_user: UserBase = Depends(get_current_user),
                                        db: Session = Depends(get_db)):
    return tender_committee.get_tender_committee_recommendation_by_request_no(request_no, db)


@router.patch("/TenderCommitteeRequest/{request_no}", response_model=u_schemas.ReturnSuccess)
async def update_tender_committee_request(request: schemas.UpdateTenderCommitteeRequest,
                                          request_no: str, current_user: UserBase = Depends(get_current_user),
                                          db: Session = Depends(get_db)):
    tender_committee.update_tender_committee_request(param=request, request_no=request_no,
                                                     current_user=current_user, db=db)
    return response_success(data={'request_no': request_no})

