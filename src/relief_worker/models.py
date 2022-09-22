import uuid
from email.policy import default

from sqlalchemy import JSON, Boolean, Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from relief_worker.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    token = Column(String, nullable=False, index=True)
    role = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    location = Column(String, nullable=False)
    min_rate = Column(Float)
    max_distance = Column(Integer, default=0)

    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"))
    company = relationship("Company", back_populates="users")
    history = relationship("ShiftAction", back_populates="user")


class Company(Base):
    __tablename__ = "companies"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String)
    region_id = Column(UUID(as_uuid=True), ForeignKey("regions.id"))
    address = Column(String)
    phone = Column(String)
    is_active = Column(Boolean, default=True)

    region = relationship("Region", back_populates="companies")
    users = relationship("User", back_populates="company")
    groups = relationship("Group", back_populates="company")
    shifts = relationship("Shift", back_populates="company")


class Group(Base):
    __tablename__ = "groups"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"))

    company = relationship("Company", back_populates="groups")
    shifts = relationship("Shift", back_populates="group")


class Region(Base):
    __tablename__ = "regions"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String)
    parent_id = Column(UUID(as_uuid=True), ForeignKey("regions.id"))

    companies = relationship("Company", back_populates="region")


class Shift(Base):
    __tablename__ = "shifts"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    rate = Column(Float, nullable=False)
    multiplier = Column(Float, default=1.0)
    role = Column(String, nullable=False)
    reqs = Column(JSON, default={})
    priority = Column(Integer, default=0)
    status = Column(String, nullable=False)

    group_id = Column(UUID(as_uuid=True), ForeignKey("groups.id"), index=True)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), index=True)
    superseded_by = Column(UUID(as_uuid=True), ForeignKey("shifts.id"), index=True)

    actions = relationship("ShiftAction", back_populates="shift")
    company = relationship("Company", back_populates="shifts")
    group = relationship("Group", back_populates="shifts")
    periods = relationship("Period", back_populates="shift")


class Period(Base):
    __tablename__ = "periods"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    start = Column(DateTime)
    end = Column(DateTime)
    overnight = Column(Boolean, default=False)

    shift_id = Column(UUID(as_uuid=True), ForeignKey("shifts.id"))
    shift = relationship("Shift", back_populates="periods")


class CompanyWorkers(Base):
    __tablename__ = "company_workers"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    is_admin = Column(Boolean, default=False)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"))
    worker_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))


class GroupWorkers(Base):
    __tablename__ = "group_workers"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    is_admin = Column(Boolean, default=False)
    group_id = Column(UUID(as_uuid=True), ForeignKey("groups.id"))
    worker_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))

    # group = relationship("Group", back_populates="workers")
    # worker = relationship("User", back_populates="groups")


class ShiftAction(Base):
    __tablename__ = "shift_actions"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    shift_id = Column(UUID(as_uuid=True), ForeignKey("shifts.id"))
    worker_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    action = Column(String)
    timestamp = Column(DateTime)

    shift = relationship("Shift", back_populates="actions")
    user = relationship("User", back_populates="history")
