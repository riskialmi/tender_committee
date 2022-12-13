import sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, text
from sqlalchemy.sql.expression import cast
from fastapi import HTTPException, status
import requests
from datetime import datetime
from app.db.models import user_management as models, reference_data as ref_models
from app.system.config import URL_EMPLOYEE_BY_USERNAME, EMAIL_ADMIN
from app.api.schemas.utils import validation_update_value_not_exist
from app.auth.hash import Hash
from app.system.email import send_email
from app.api.crud.utils import random_alphanumeric
from fastapi.exceptions import RequestValidationError
import json
import pytz

ua = models.UserAccount
msl = ref_models.MsLookup
mm = ref_models.MasterMenu
mma = ref_models.MasterMenuAssignment
ur = models.UserRoles
keob = models.K2EmployeeOnBoarding


def get_user_position_by_account_name(account_name):
    response = requests.get(URL_EMPLOYEE_BY_USERNAME + account_name)

    if response.status_code == 200:
        response = response.json()
        return {'directorate': response['directorate_findim_code'],
                'division': response['division_findim_code'],
                'department_id': response['department_id']}

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f'Error get data employee with username {account_name}')


def get_list_user(param, db: Session):
    result = []

    accounts = db.query(ua.account_name,
                        ua.title,
                        ua.first_name,
                        ua.middle_name,
                        ua.last_name,
                        msl.name.label("status")
                        ) \
        .join(ref_models.MsLookup, and_(msl.type == "UserStatus", msl.value == ua.status), isouter=True) \
        .order_by(text(param.sortColumnDir + " " + param.sortColumn)) \
        .limit(param.pageSize) \
        .offset((param.pageNumber - 1) * param.pageSize) \
        .all()

    for a in accounts:
        a = dict(a)
        data = get_user_position_by_account_name(a['account_name'])
        a['directorate'] = data['directorate']
        a['division'] = data['division']

        result.append(a)

    return result


def get_user_by_account_name(account_name, db: Session):
    user = db.query(models.UserAccount).filter(ua.account_name == account_name).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"username {account_name} doesn't exist")
    return user


def get_user_by_email(email, db: Session):
    user = db.query(models.UserAccount).filter(ua.email == email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"email {email} doesn't exist")
    return user


def get_payload_token_by_username(username, on_behalf_of, db: Session):
    # data = get_division_and_directorate_by_account_name(username)

    payload = dict(db.query(ua.account_name,
                            func.rtrim(func.concat(func.rtrim(func.concat(ua.first_name, ' ', ua.middle_name)),
                                                   ' ', ua.last_name)).label("full_name"),
                            ua.email,
                            ua.title.label("employee_role"),
                            func.string_agg(models.MasterRole.role_name, ',').label("list_role")
                            ) \
                   .join(models.UserRoles, ur.account_name == ua.account_name, isouter=True) \
                   .join(models.MasterRole, models.MasterRole.id == models.UserRoles.role_id, isouter=True) \
                   .filter(ua.account_name == username) \
                   .group_by(ua.account_name) \
                   .first())

    # payload['division'] = data['division']
    # payload['directorate'] = data['directorate']
    payload['on_behalf_of'] = on_behalf_of

    return payload


def get_k2_employee_by_account_name(account_name, db: Session):
    user = db.query(keob).filter(
        keob.account_name == account_name).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"username {account_name} doesn't exist")
    return user


def get_details_k2_employee_onboarding_by_account_name(account_name, db: Session):
    user_info = dict(db.query(keob.account_name,
                              keob.full_name,
                              keob.role_name,
                              keob.email,
                              keob.employee_number.label("employee_no"),
                              keob.ax_worker_number.label("ax_worker_no"),
                              keob.bank_name,
                              keob.branch_name,
                              keob.bank_account_no,
                              keob.bank_account_name,
                              keob.registered_on
                              ) \
                     .filter(keob.account_name == account_name) \
                     .group_by(keob.account_name) \
                     .first())

    user_info['first_name'] = None
    user_info['middle_name'] = None
    user_info['last_name'] = None
    middle = []

    full_name = user_info['full_name'].split(" ")

    user_info['first_name'] = full_name[0]
    if len(full_name) == 2:
        user_info['last_name'] = full_name[-1]
    elif len(full_name) > 2:
        user_info['last_name'] = full_name[-1]
        for a in full_name:
            if a not in user_info['first_name'] and a not in user_info['last_name']:
                middle.append(a)
            user_info['middle_name'] = " ".join(middle)

    return user_info


def get_k2_employee_onboarding_except_user_list(db: Session):
    return db.query(keob.account_name.label("text"),
                    keob.account_name.label("value")
                    ) \
        .join(models.UserAccount, ua.account_name == keob.account_name, isouter=True) \
        .filter(ua.account_name == None) \
        .all()


def get_details_user_account_by_account_name(account_name, db: Session):
    user_info = dict(db.query(ua.account_name,
                              func.rtrim(func.concat(func.rtrim(func.concat(ua.first_name, ' ', ua.middle_name)),
                                                     ' ', ua.last_name)).label("full_name"),
                              ua.first_name,
                              ua.middle_name,
                              ua.last_name,
                              ua.title.label('role_name'),
                              ua.email,
                              ua.employee_number.label('employee_no'),
                              ua.ax_personel_number.label('ax_worker_no'),
                              ua.bank_name,
                              ua.branch_name,
                              ua.bank_account_no,
                              ua.bank_account_name,
                              ua.registered_on,
                              func.string_agg(cast(ur.role_id, sqlalchemy.String), ',').label('roles')
                              ) \
                     .join(models.UserRoles, ur.account_name == ua.account_name, isouter=True) \
                     .filter(ua.account_name == account_name) \
                     .group_by(ua.account_name) \
                     .first())

    if user_info['roles']:
        user_info['roles'] = user_info['roles'].split(',')

    return user_info


def create_user_roles(roles, account_name, db: Session):
    for r in roles:
        role = models.UserRoles(role_id=r, account_name=account_name)
        db.add(role)


def create_random_password_hash(size):
    pass_ran = random_alphanumeric(size)
    return {'pass_hash': Hash.bcrypt(pass_ran),
            'pass_ran': pass_ran}


def create_user_account(param, db: Session):
    password = create_random_password_hash(size=8)
    user_account = models.UserAccount(account_name=param.account_name, title=param.role_name,
                                      first_name=param.first_name, middle_name=param.middle_name,
                                      last_name=param.last_name, email=param.email,
                                      ax_personel_number=param.ax_worker_no, registered_on=param.registered_on,
                                      ax_personel_name=param.full_name, status=1, password_hash=password['pass_hash'],
                                      employee_number=param.employee_no, bank_name=param.bank_name,
                                      branch_name=param.branch_name, bank_account_no=param.bank_account_no,
                                      bank_account_name=param.bank_account_name)

    create_user_roles(param.roles, user_account.account_name, db)
    create_hist_user_roles(param.roles, user_account, db)
    db.commit()
    db.refresh(user_account)

    send_pass_to_email(password['pass_ran'], EMAIL_ADMIN, user_account.account_name)

    return user_account


def update_pass_hash(account_name, db: Session):
    user = get_user_by_account_name(account_name, db)
    json_user = get_user_audittrail(user)
    password = create_random_password_hash(size=8)

    user_account = db.query(models.UserAccount).filter(models.UserAccount.account_name == account_name)
    user_account.update({models.UserAccount.password_hash: password['pass_hash'],
                         models.UserAccount.user_audittrail: json_user})
    db.commit()

    send_pass_to_email(password['pass_ran'], ['v-ralmi@iif.co.id'], account_name)


def delete_user_account_by_account_name(account_name, db: Session):
    user = get_user_by_account_name(account_name, db)
    json_user = get_user_audittrail(user)
    user_account = db.query(models.UserAccount).filter(models.UserAccount.account_name == account_name)

    user_account.update(
        {models.UserAccount.status: 2, models.UserAccount.updated_dtm: datetime.now(pytz.timezone('Asia/Jakarta')),
         models.UserAccount.user_audittrail: json_user})
    db.commit()


def send_pass_to_email(password, email, username):
    msg = '''\
        Password user {username} is <b>{password}</b>
    '''.format(username=username,
               password=password)

    send_email(to=email, subject=f'Password username {username}', message=msg, file_name=None, attach_bytes=None)


def delete_user_roles_by_account_name(account_name, db: Session):
    return db.query(models.UserRoles).filter_by(account_name=account_name).delete()


def create_hist_user_roles(roles, user_account, db: Session):
    for r in roles:
        master_role = db.query(models.MasterRole).filter_by(id=r).first()
        hist_user_role = models.HistoryUserRoles(account_name=user_account.account_name, role_id=r,
                                                 role_name=master_role.role_name, user_account=user_account)
        db.add(hist_user_role)


def get_user_audittrail(user):
    user_audittrail = user.user_audittrail
    user = user.__dict__
    user.pop('user_audittrail')
    json_user = json.dumps(user, default=str)
    json_load_user = json.loads(json_user)

    if user_audittrail:
        user_audittrail.append(json_load_user)
        return user_audittrail
    else:
        return [json_load_user]


def update_user_account(param, db: Session):
    user = get_user_by_account_name(param.account_name, db)
    json_user = get_user_audittrail(user)

    user_account = db.query(models.UserAccount).filter(models.UserAccount.account_name == param.account_name)

    user_account.update({ua.bank_name: param.bank_name, ua.branch_name: param.branch_name,
                         ua.bank_account_no: param.bank_account_no, ua.bank_account_name: param.bank_account_name,
                         ua.updated_dtm: datetime.now(pytz.timezone('Asia/Jakarta')), ua.user_audittrail: json_user})

    delete_user_roles_by_account_name(param.account_name, db)
    create_user_roles(param.roles, param.account_name, db)
    create_hist_user_roles(param.roles, user_account, db)

    db.commit()

    return user_account


def get_user_menu_by_account_name(account_name, db: Session):
    return db.query(func.distinct(mm.id).label("id"),
                    mm.menu_name,
                    mm.menu_route,
                    mm.icon,
                    mm.sequence,
                    mm.parent_id
                    ) \
        .join(ref_models.MasterMenuAssignment, mma.menu_id == mm.id, isouter=True) \
        .join(models.UserRoles, ur.role_id == mma.role_id) \
        .filter(and_(mm.is_visible == True, mm.is_deleted == False,
                     ur.account_name == account_name)) \
        .all()


def get_active_user_account(db: Session):
    return db.query(ua.account_name.label('text'), ua.account_name.label('value')).filter(ua.status == 1).all()


def get_user_information_by_account_name(account_name, db: Session):
    user_account = dict(db.query(func.rtrim(func.concat(func.rtrim(func.concat(ua.first_name, ' ', ua.middle_name)),
                                                        ' ', ua.last_name)).label("name"),
                                 ua.email
                                 ) \
                        .filter(and_(ua.status == 1, ua.account_name == account_name)) \
                        .first())

    if not user_account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"username {account_name} doesn't exist")

    data = get_user_position_by_account_name(account_name)
    user_account['directorate'] = data['directorate']
    user_account['division'] = data['division']

    return user_account


def get_user_by_role_name(role_name, db: Session):
    user = db.query(func.string_agg(models.UserAccount.account_name, ', ').label("account_name")) \
        .join(models.UserRoles, ur.account_name == ua.account_name, isouter=True) \
        .join(models.MasterRole, models.MasterRole.id == ur.role_id, isouter=True) \
        .filter(models.MasterRole.role_name == role_name) \
        .first()

    return user.account_name
