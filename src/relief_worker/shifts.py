from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from relief_worker import models, schemas
from relief_worker.db import get_db
from relief_worker.user import get_current_user

router = APIRouter()


@router.post("/search", response_model=list[schemas.Shift])
def view_company_shifts(filter, db: Session = Depends(get_db)):
    ...


@router.put("/create", response_model=schemas.Shift)
def create_shift(shift, db: Session = Depends(get_db)):
    ...


@router.get("/{shift_id}", response_model=schemas.Shift)
def view_shift(shift_id: str, db: Session = Depends(get_db)):
    ...


@router.post("/{shift_id}/apply")
def apply_shift(
    shift_id: str,
    db: Session = Depends(get_db),
    user: schemas.User = Depends(get_current_user),
):
    ...


def add_shift(db: Session, shift: schemas.ShiftCreate, periods: list[schemas.PeriodCreate]):
    new_shift = models.Shift(**shift.dict(exclude_none=True))
    db.add(new_shift)
    db.commit()
    db.refresh(new_shift)
    new_periods = []
    for p in periods:
        np = models.Period(**p.dict(exclude_none=True), shift_id=new_shift.id)
        new_periods.append(np)
    db.add_all(new_periods)
    db.commit()


def create_period(db: Session, period: schemas.PeriodCreate):
    db.add(**period.dict(exclude_none=True))
