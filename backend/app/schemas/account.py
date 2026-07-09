from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import AccountType


class CreateAccountRequest(BaseModel):
    name: str = Field(default=None, min_length=2, max_length=100)
    institution: str = Field(default=None, min_length=2, max_length=100)
    type: AccountType
    currency: str = Field(default="INR", min_length=3, max_length=3)


class AccountResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    name: str
    institution: str
    type: AccountType
    currency: str
    created_at: datetime
    updated_at: datetime


class UpdateAccountRequest(BaseModel):
    name: str = Field(default=None, min_length=2, max_length=100)
    institution: str = Field(default=None, min_length=2, max_length=100)
    type: AccountType
    currency: str = Field(default="INR", min_length=3, max_length=3)
