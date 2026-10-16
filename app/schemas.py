from datetime import date, datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class ApplicationStatus(str, Enum):
    APPLIED = "Applied"
    INTERVIEW = "Interview"
    OFFER = "Offer"
    REJECTED = "Rejected"
    WITHDRAWN = "Withdrawn"


class JobApplicationCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    company: str = Field(min_length=1, max_length=150)
    role: str = Field(min_length=1, max_length=150)
    application_date: date
    status: ApplicationStatus = ApplicationStatus.APPLIED
    notes: str | None = None


class JobApplicationUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    company: str | None = Field(
        default=None,
        min_length=1,
        max_length=150,
    )
    role: str | None = Field(
        default=None,
        min_length=1,
        max_length=150,
    )
    application_date: date | None = None
    status: ApplicationStatus | None = None
    notes: str | None = None


class JobApplicationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    company: str
    role: str
    application_date: date
    status: ApplicationStatus
    notes: str | None
    created_at: datetime
    updated_at: datetime
