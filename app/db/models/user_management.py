from sqlalchemy import Column
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func, expression
from sqlalchemy.sql.sqltypes import Integer, Numeric, String, Boolean, Date, DateTime, JSON, DECIMAL
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from app.db.models.reference_data import MasterRole

Base = declarative_base()

class UserAccount(Base):
    __tablename__ = "user_account"
    account_name = Column(String(20), primary_key=True)
    title = Column(String(10))
    first_name = Column(String(50))
    middle_name = Column(String(50))
    last_name = Column(String(50))
    email = Column(String(50))
    password_hash = Column(String(2000))
    ax_personel_number = Column(String(50))
    ax_personel_name = Column(String(50))
    employee_number = Column(String(12))
    registered_on = Column(DateTime)
    status = Column(Integer)
    bank_name = Column(String(50))
    branch_name = Column(String(50))
    bank_account_name = Column(String(70))
    bank_account_no = Column(String(20))
    last_login = Column(DateTime)
    created_dtm = Column(DateTime(timezone=True), server_default=func.now())
    updated_dtm = Column(DateTime)
    user_audittrail = Column(JSON)

    hist_user_roles = relationship("HistoryUserRoles", backref="user_account")
    user_role = relationship("UserRoles", backref="user_account")

class UserTxnReviewer(Base):
    __tablename__ = "user_txn_reviewer"
    id = Column(Integer, primary_key=True)
    txn_type = Column(String)
    step = Column(Integer)
    account_name_requester = Column(String(20), ForeignKey("user_account.account_name"))
    account_name_reviewer = Column(String(20), ForeignKey("user_account.account_name"))
    reviewer_role_name = Column(String)
    created_dtm = Column(DateTime(timezone=True), server_default=func.now())
    updated_dtm = Column(DateTime)
    user_audittrail = Column(JSON)

class UserRoles(Base):
    __tablename__ = "user_roles"
    id = Column(Integer, primary_key=True)
    role_id = Column(Integer, ForeignKey(MasterRole.id))
    account_name = Column(String(20), ForeignKey(UserAccount.account_name))
    created_dtm = Column(DateTime(timezone=True), server_default=func.now())
    updated_dtm = Column(DateTime)


class HistoryUserRoles(Base):
    __tablename__ = "hist_user_roles"
    id = Column(Integer, primary_key=True)
    account_name = Column(String(20), ForeignKey(UserAccount.account_name))
    role_id = Column(Integer, ForeignKey(MasterRole.id))
    role_name = Column(String(50))
    created_dtm = Column(DateTime(timezone=True), server_default=func.now())
    updated_dtm = Column(DateTime)
    # user_audittrail = Column(String(1000))


class DelegationBackoffice(Base):
    __tablename__ = "delegation_backoffice"
    guid = Column(String, primary_key=True)
    txn_type = Column(String(50))
    amount_min = Column(DECIMAL(scale=2, precision=18))
    amount_max = Column(DECIMAL(scale=2, precision=18))
    granted_by = Column(String(20), ForeignKey("user_account.account_name"))
    granted_from = Column(DateTime)
    granted_until = Column(DateTime)
    granted_account = Column(JSON)
    is_active = Column(Boolean)
    created_dtm = Column(DateTime, server_default=func.now())
    updated_dtm = Column(DateTime)

class DelegationTransaction(Base):
    __tablename__ = "delegation_transaction"
    guid = Column(String, primary_key=True)
    txn_type = Column(String(50))
    amount_min = Column(DECIMAL(scale=2, precision=18))
    amount_max = Column(DECIMAL(scale=2, precision=18))
    granted_by = Column(String(20), ForeignKey("user_account.account_name"))
    granted_from = Column(DateTime)
    granted_until = Column(DateTime)
    onbehalfof_users = Column(JSON)
    is_active = Column(Boolean)
    created_dtm = Column(DateTime, server_default=func.now())
    updated_dtm = Column(DateTime)

class DelegationRole(Base):
    __tablename__ = "delegation_role"
    guid = Column(String, primary_key=True)
    onbehalfof_users = Column(String(20), ForeignKey("user_account.account_name"))
    delegated_role = Column(Integer, ForeignKey(MasterRole.id))
    account_name = Column(String(20), ForeignKey("user_account.account_name"))
    granted_by = Column(String(20), ForeignKey("user_account.account_name"))
    granted_from = Column(DateTime)
    granted_until = Column(DateTime)
    granted_menu = Column(JSON)
    is_active = Column(Boolean)
    created_dtm = Column(DateTime, server_default=func.now())
    updated_dtm = Column(DateTime)

class LogSession(Base):
    __tablename__ = "log_session"
    id = Column(Integer, primary_key=True)
    user_name = Column(String(20), ForeignKey("user_account.account_name"))
    full_name = Column(String(70))
    ip_address = Column(String(20))
    info_login = Column(String)
    created_dtm = Column(DateTime(timezone=True), server_default=func.now())

class LogActivity(Base):
    __tablename__ = "log_activity"
    id = Column(Integer, primary_key=True)
    user_name = Column(String(20), ForeignKey("user_account.account_name"))
    full_name = Column(String(70))
    jwt_access = Column(String)
    activity = Column(JSON)
    menu = Column(String)
    created_dtm = Column(DateTime(timezone=True), server_default=func.now())

class K2EmployeeOnBoarding(Base):
    __tablename__ = "k2_employee_on_boarding"
    account_name = Column(String(20), primary_key=True)
    full_name = Column(String(70))
    role_name = Column(String(50))
    email = Column(String(50))
    employee_number = Column(String(12))
    ax_worker_number = Column(String(12))
    bank_name = Column(String(50))
    branch_name = Column(String(50))
    bank_account_name = Column(String(70))
    bank_account_no = Column(String(20))
    registered_on = Column(DateTime)
    created_dtm = Column(DateTime(timezone=True), server_default=func.now())
    updated_dtm = Column(DateTime)

