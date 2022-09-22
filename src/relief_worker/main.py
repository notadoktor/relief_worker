import datetime

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from relief_worker import company, db, models, schemas, shifts, user
from relief_worker.util import verify_key, verify_token

models.Base.metadata.create_all(bind=db.engine)


app = FastAPI()
app.include_router(
    company.router,
    prefix="/company",
    tags=["company"],
)
app.include_router(
    shifts.router,
    prefix="/shifts",
    tags=["shifts"],
)
app.include_router(
    user.router,
    prefix="/user",
    tags=["user"],
)


@app.post("/login", response_model=schemas.UserToken)
def login(creds: schemas.UserLogin, db: Session = Depends(db.get_db)):
    token = user.auth_user(db, creds)
    if not token:
        raise HTTPException(status_code=400, detail="Invalid user credentials")
    return {"token": token}


@app.get("/ping")
def ping():
    return {"message": "pong", "ts": str(datetime.datetime.now())}
