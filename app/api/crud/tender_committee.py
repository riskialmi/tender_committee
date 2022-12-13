import sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy import func, or_, text
from sqlalchemy.sql.expression import cast
from app.db.models import tender_committee as models
from app.api.crud import utils, user_management
from app.system.constant import initial_status_tender_committee
from fastapi import HTTPException, status

tcr = models.TenderCommitteeRequest
tcrc = models.TenderCommitteeRecommendation
tc = models.TenderCommittee


def get_list_active_tender_committee(param, db: Session):
    return db.query(tc.id,
                    tc.account_name,
                    tc.name,
                    tc.email,
                    tc.directorate,
                    tc.division,
                    tc.effective_start_date.label('start_date'),
                    tc.effective_end_date.label('end_date'),
                    tc.is_active
                    ) \
        .filter(or_(tc.is_active == True, cast(tc.effective_end_date, sqlalchemy.Date) >= func.current_date())) \
        .order_by(text(param.sortColumnDir + " " + param.sortColumn)) \
        .limit(param.pageSize) \
        .offset((param.pageNumber - 1) * param.pageSize) \
        .all()


def create_tender_committee_recommendation(recommendations, tcr_obj, user_login, db: Session):
    # bypass
    role = {'department_id': 'TEST'}

    for r in recommendations:
        # role = user_management.get_user_position_by_account_name(r.account_name)
        recommendation = models.TenderCommitteeRecommendation(tender_committee_request_id=tcr_obj.id,
                                                              account_name=r.account_name, name=r.name, email=r.email,
                                                              directorate=r.directorate, division=r.division,
                                                              created_by=user_login, department=role['department_id'],
                                                              tender_committee_request=tcr_obj
                                                              )

        db.add(recommendation)


def create_tender_committee_request(param, current_user, db: Session):
    request_no = utils.generate_request_no(code='TC')

    tcr_obj = models.TenderCommitteeRequest(request_no=request_no, agns_number=param.agns_number,
                                            memo_to=param.memo_to, on_behalf_of=current_user['on_behalf_of'],
                                            subject=param.subject, effective_start_date=param.effective_start_date,
                                            effective_end_date=param.effective_end_date, created_by=current_user['user'],
                                            letter=param.letter, status=initial_status_tender_committee,
                                            )

    db.add(tcr_obj)
    create_tender_committee_recommendation(param.recommendation, tcr_obj, current_user['user'], db)
    db.commit()
    return tcr_obj


def delete_tender_committee_recommendation_by_request_no(request_no, db: Session):
    return db.query(models.TenderCommitteeRecommendation).filter_by(request_no=request_no).delete()


def update_tender_committee_recommendation(tender_committee_recommendations, db):
    for tcr in tender_committee_recommendations:
        tender_committee_recommendation = db.get(models.TenderCommitteeRecommendation, tcr.id)
        param_data = tcr.dict(exclude_unset=True)

        for key, value in param_data.items():
            setattr(tender_committee_recommendation, key, value)

        db.add(tender_committee_recommendation)

def update_tender_committee_request(param, request_no, current_user, db: Session):
    tender_committee_request = get_tender_committee_request_by_request_no(request_no, db)
    param_data = param.dict(exclude_unset=True)

    for key, value in param_data.items():
        setattr(tender_committee_request, key, value)
    setattr(tender_committee_request, 'updated_by', current_user['user'])

    if param.recommendation:
        update_tender_committee_recommendation(param.recommendation,  db)

    db.commit()


def get_tender_committee_request_by_request_no(request_no, db: Session):
    data_tcr = db.query(models.TenderCommitteeRequest).filter(tcr.request_no == request_no).first()

    if not data_tcr:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Request number {request_no} doesn't exist")

    return data_tcr


def get_tender_committee_recommendation_by_request_no(request_no, db: Session):
    data = db.query(models.TenderCommitteeRecommendation)\
        .join(models.TenderCommitteeRequest, tcr.id == tcrc.tender_committee_request_id)\
        .filter(tcr.request_no == request_no)\
        .all()

    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Data not found with request number {request_no}")

    return data

def get_tender_committee_by_id(id, db: Session):
    tc_obj = db.query(tc.id,
                      tc.account_name,
                      tc.name,
                      tc.email,
                      tc.directorate,
                      tc.division,
                      tc.effective_start_date.label('start_date'),
                      tc.effective_end_date.label('end_date'),
                      tc.is_active
                      ) \
        .filter(tc.id == id) \
        .first()

    if not tc_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"id {id} doesn't exist")

    return tc_obj


def update_tender_committee(tender_committee_id, param, db: Session):
    tender_committee = db.get(models.TenderCommittee, tender_committee_id)

    if not tender_committee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"id {tender_committee_id} doesn't exist")

    for key, value in param.dict().items():
        setattr(tender_committee, key, value)

    db.add(tender_committee)
    db.commit()

def delete_tender_committee_by_id(id, db: Session):
    get_tender_committee_by_id(id, db)
    tc = db.query(models.TenderCommittee).filter(models.TenderCommittee.id == id)

    tc.update({models.TenderCommittee.is_active: False})
    db.commit()


def update_status_tender_committee_request(request_no, current_status, db):
    tcr_obj = db.query(models.TenderCommitteeRequest).filter(tcr.request_no == request_no)

    tcr_obj.update({tcr.status: current_status})
    db.commit()


def get_data_tender_committee_by_request_no(request_no, db: Session):
    return db.query(tcrc.account_name,
                    tcrc.name,
                    tcrc.email,
                    tcrc.directorate,
                    tcrc.division,
                    tcr.effective_start_date,
                    tcr.effective_end_date
                    ) \
        .join(models.TenderCommitteeRequest, tcr.request_no == tcrc.request_no, isouter=True) \
         .filter(tcrc.request_no == request_no) \
        .all()


def create_tender_committee(param):
    return models.TenderCommittee(account_name=param.account_name, name=param.name, email=param.email,
                                  directorate=param.directorate, division=param.division,
                                  effective_start_date=param.start_date, effective_end_date=param.end_date)


def create_tender_committee_log(param):
    return models.TenderCommitteeLog(account_name=param.account_name, name=param.name, email=param.email,
                                     directorate=param.directorate, division=param.division,
                                     effective_start_date=param.effective_start_date, tender_committee_id=param.id,
                                     effective_end_date=param.effective_end_date, tender_committee=param)
