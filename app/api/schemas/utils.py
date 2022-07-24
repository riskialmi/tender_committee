from typing import Optional, Tuple, Dict, Any
from pydantic import BaseModel
from pydantic.error_wrappers import ErrorWrapper
from pydantic.main import ModelMetaclass


def validation_update_value_already_exist(value):
    return ErrorWrapper(Exception(f'{value} already exist'), ("body", value))


def validation_update_value_not_exist(value):
    return ErrorWrapper(Exception(f'{value} does not exist'), ("body", value))


class Pagination(BaseModel):
    sortColumn: str
    sortColumnDir: str
    pageNumber: int
    pageSize: int


class DropDown(BaseModel):
    text: str
    value: str

    class Config:
        orm_mode = True


class ReturnSuccess(BaseModel):
    is_success: bool
    data: Optional[dict] = None
    message: Optional[str] = None

    class Config:
        orm_mode = True


class _AllOptionalMeta(ModelMetaclass):
    def __new__(self, name: str, bases: Tuple[type], namespaces: Dict[str, Any], **kwargs):
        annotations: dict = namespaces.get('__annotations__', {})

        for base in bases:
            for base_ in base.__mro__:
                if base_ is BaseModel:
                    break

                annotations.update(base_.__annotations__)

        for field in annotations:
            if not field.startswith('__'):
                annotations[field] = Optional[annotations[field]]

        namespaces['__annotations__'] = annotations

        return super().__new__(self, name, bases, namespaces, **kwargs)
