from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class ListUser(BaseModel):
    account_name: str
    title: str
    first_name: str
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    directorate: Optional[str] = None
    division: Optional[str] = None
    status: str

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    username: str
    password: str

class K2EemployeeOnboarding(BaseModel):
    account_name: str
    full_name: str
    role_name: str
    email: str
    employee_no: Optional[str] = None
    ax_worker_no: str
    bank_name: Optional[str] = None
    branch_name: Optional[str] = None
    bank_account_no: Optional[str] = None
    bank_account_name: Optional[str] = None
    registered_on: Optional[datetime] = None

    class Config:
        orm_mode = True

class AccountInformation(K2EemployeeOnboarding):
    first_name: str
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    roles: list

    class Config:
        orm_mode = True

class UpdateAccountInformation(AccountInformation):
    id: int

    class Config:
        orm_mode = True

class UserMenu(BaseModel):
    id: int
    menu_name: str
    menu_route: str
    icon: Optional[str] = None
    sequence: Optional[int] = None
    parent_id: Optional[int] = None

    class Config:
        orm_mode = True

