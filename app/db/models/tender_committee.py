from sqlalchemy import Column
from sqlalchemy.sql import func, expression
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Integer, LargeBinary, String, Boolean, Date, DateTime, JSON, DECIMAL
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class TenderCommitteeRequest(Base):
    __tablename__ = "tender_committee_request"
    id = Column(Integer, primary_key=True)
    request_no = Column(String(20))
    agns_number = Column(String(20))
    memo_to = Column(String(12))
    subject = Column(String(100))
    effective_start_date = Column(DateTime)
    effective_end_date = Column(DateTime)
    letter = Column(LargeBinary)
    status = Column(String(20))
    on_behalf_of = Column(String(12))
    created_by = Column(String(12))
    updated_by = Column(String(12))
    created_dtm = Column(DateTime(timezone=True), server_default=func.now())
    updated_dtm = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    tender_committee_recommendation = relationship("TenderCommitteeRecommendation", backref="tender_committee_request")

class TenderCommitteeRecommendation(Base):
    __tablename__ = "tender_committee_recommendation"
    id = Column(Integer, primary_key=True)
    tender_committee_request_id = Column(Integer, ForeignKey(TenderCommitteeRequest.id), nullable=False)
    account_name = Column(String(12))
    name = Column(String(50))
    email = Column(String(50))
    directorate = Column(String(5))
    division = Column(String(10))
    department = Column(String(10))
    created_by = Column(String(12))
    created_dtm = Column(DateTime(timezone=True), server_default=func.now())

class TenderCommittee(Base):
    __tablename__ = "tender_committee"
    id = Column(Integer, primary_key=True)
    account_name = Column(String(12))
    name = Column(String(50))
    email = Column(String(50))
    directorate = Column(String(5))
    division = Column(String(10))
    effective_start_date = Column(DateTime)
    effective_end_date = Column(DateTime)
    is_active = Column(Boolean, server_default=expression.true())
    created_dtm = Column(DateTime(timezone=True), server_default=func.now())

    tender_committee_log = relationship("TenderCommitteeLog", backref="tender_committee")

class TenderCommitteeLog(Base):
    __tablename__ = "tender_committee_log"
    id = Column(Integer, primary_key=True)
    tender_committee_id = Column(Integer, ForeignKey("tender_committee.id"))
    account_name = Column(String(20))
    name = Column(String(50))
    email = Column(String(50))
    directorate = Column(String(5))
    division = Column(String(10))
    effective_start_date = Column(DateTime)
    effective_end_date = Column(DateTime)
    is_active = Column(Boolean, server_default=expression.true())
    created_dtm = Column(DateTime(timezone=True), server_default=func.now())
