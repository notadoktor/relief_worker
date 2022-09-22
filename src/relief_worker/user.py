import uuid
from operator import and_

from fastapi import APIRouter, Depends, Header
from sqlalchemy import and_
from sqlalchemy.orm import Session

from relief_worker import schemas
from relief_worker.db import get_db
from relief_worker.models import User

router = APIRouter()


@router.post("/logout")
def logout(token: str = Header("token")):
    ...


@router.post("/register")
def register():
    ...


@router.get("/profile/{user_id}", response_model=schemas.User)
def view_profile(user_id: str, db: Session = Depends(get_db)):
    ...


@router.post("/profile/{user_id}/edit", response_model=schemas.User)
def edit_profile(user_id: str, db: Session = Depends(get_db)):
    ...


@router.get("/profile/{user_id}/shifts", response_model=list[schemas.Shift])
def view_shifts(user_id: str, db: Session = Depends(get_db)):
    ...


def auth_user(db: Session, creds: schemas.UserLogin):
    u: User | None = (
        db.query(User)
        .filter(and_(User.email == creds.email, User.password == creds.password))
        .first()
    )
    if u:
        return u.token


def get_user(
    db: Session, *, user_id: str | None = None, email: str | None = None, token: str | None = None
):
    if user_id:
        return db.query(User).filter(User.id == user_id).first()
    elif email:
        return db.query(User).filter(User.email == email).first()
    elif token:
        return db.query(User).filter(User.token == token).first()
    return None


def get_current_user(token: str = Header("token"), db: Session = Depends(get_db)):
    return get_user(db, token=token)


def create_user(db: Session, user: schemas.UserCreate):
    db_user = User(**user.dict(), token=str(uuid.uuid4()))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
