from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Json, ValidationError, validator, create_model, EmailStr
from pydantic.error_wrappers import ErrorWrapper

class Login(BaseModel):
    username: str
    password: str
    onBehalf: Optional[str] = False
    onAccountOf: Optional[str] = None

    class Config:
        orm_mode = True
