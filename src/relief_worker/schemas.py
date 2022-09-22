from __future__ import annotations

import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from relief_worker.enums import *


class UserBase(BaseModel):
    name: str
    email: str
    phone: str
    role: WorkerRole
    location: str
    is_active: bool = True
    min_rate: float | None = None
    max_distance: int = 0


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: UUID

    class Config:
        orm_mode = True


class UserFull(User):
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class UserToken(BaseModel):
    token: str


class CompanyBase(BaseModel):
    name: str
    address: str
    phone: str
    is_active: bool = True


class CompanyCreate(CompanyBase):
    region_id: UUID


class Company(CompanyBase):
    id: UUID
    region: Region

    class Config:
        orm_mode = True


class GroupBase(BaseModel):
    name: str
    company_id: str


class GroupCreate(GroupBase):
    pass


class Group(GroupBase):
    id: UUID
    company: Company

    @property
    def company_name(self):
        return self.company.name

    @property
    def region(self):
        return self.company.region

    class Config:
        orm_mode = True


class RegionBase(BaseModel):
    name: str
    parent_id: UUID | None = None


class RegionCreate(RegionBase):
    pass


class Region(RegionBase):
    id: UUID

    class Config:
        orm_mode = True


class ShiftBase(BaseModel):
    name: str
    rate: float
    multiplier: float
    role: WorkerRole
    reqs: dict
    priority: int
    status: ShiftStatus
    periods: list[Period] = Field(default_factory=list)


class ShiftCreate(ShiftBase):
    company_id: str
    group_id: str


class Shift(ShiftBase):
    id: UUID
    group: Group
    company: Company
    actions: list[ShiftAction] = Field(default_factory=list)

    class Config:
        orm_mode = True


class BasePeriod(BaseModel):
    start: datetime.datetime
    end: datetime.datetime
    overnight: bool = False


class PeriodCreate(BasePeriod):
    pass


class Period(BasePeriod):
    id: UUID
    shift_id: str

    class Config:
        orm_mode = True
