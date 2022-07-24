from sqlalchemy import Column
from sqlalchemy.sql import func, expression
from sqlalchemy.sql.sqltypes import Integer, Numeric, String, Boolean, Date, DateTime, JSON, DECIMAL, ARRAY
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class MsLookup(Base):
    __tablename__ = "master_lookup"
    id = Column(Integer, primary_key=True)
    type = Column(String)
    name = Column(String)
    value = Column(Integer)
    sequence = Column(Integer)
    is_deleted = Column(Boolean, server_default=expression.false())

class DocumentType(Base):
    __tablename__ = "document_type"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    is_deleted = Column(Boolean, server_default=expression.false())
    is_expired_date = Column(Boolean, server_default=expression.false())
    created_dtm = Column(DateTime(timezone=True), server_default=func.now())
    updated_dtm = Column(DateTime)

class CompanyType(Base):
    __tablename__ = "company_type"
    id = Column(Integer, primary_key=True)
    code = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False)
    is_deleted = Column(Boolean, server_default=expression.false())
    created_dtm = Column(DateTime(timezone=True), server_default=func.now())
    updated_dtm = Column(DateTime)

class VendorCategory(Base):
    __tablename__ = "vendor_category"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    is_deleted = Column(Boolean, server_default=expression.false())
    created_dtm = Column(DateTime(timezone=True), server_default=func.now())
    updated_dtm = Column(DateTime)

class Currency(Base):
    __tablename__ = "currency"
    id = Column(Integer, primary_key=True)
    country = Column(String, nullable=False)
    currency = Column(String, nullable=False)
    code = Column(String, nullable=False)
    is_deleted = Column(Boolean, server_default=expression.false())
    created_dtm = Column(DateTime(timezone=True), server_default=func.now())
    updated_dtm = Column(DateTime)

class MSBank(Base):
    __tablename__ = "master_bank"
    code_bank = Column(String, primary_key=True)
    bank_name = Column(String, nullable=False)
    value = Column(Integer)
    sequence = Column(Integer)
    is_deleted = Column(Boolean, server_default=expression.false())
    created_dtm = Column(DateTime(timezone=True), server_default=func.now())
    updated_dtm = Column(DateTime)

class MasterRole(Base):
    __tablename__ = "master_role"
    id = Column(Integer, primary_key=True)
    role_name = Column(String(50))
    description = Column(String(200))
    is_active = Column(Boolean, server_default=expression.true())
    created_dtm = Column(DateTime(timezone=True), server_default=func.now())
    updated_dtm = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

class MasterMenu(Base):
    __tablename__ = "master_menu"
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey("master_menu.id"))
    menu_name = Column(String(50))
    menu_route = Column(String)
    is_visible = Column(Boolean)
    icon = Column(String)
    sequence = Column(Integer)
    is_deleted = Column(Boolean, server_default=expression.false())

    master_menu_assign = relationship("MasterMenuAssignment", backref="master_menu")

class MasterMenuAssignment(Base):
    __tablename__ = "master_menu_assignment"
    id = Column(Integer, primary_key=True)
    role_id = Column(Integer, ForeignKey("master_role.id"))
    menu_id = Column(Integer, ForeignKey("master_menu.id"))
    access_level = Column(JSON)
