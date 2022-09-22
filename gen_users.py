import random
import sys
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.absolute() / "src"))

import dotenv

dotenv.load_dotenv()

from relief_worker import models, schemas
from relief_worker.db import get_db
from relief_worker.enums import *
from relief_worker.user import create_user

db = next(get_db())
REGION_IDS = {k: uuid.uuid4() for k in ["Oslo", "Østlandet", "Sør-Øst", "Norge"]}
PARENTS = {"Oslo": "Østlandet", "Østlandet": "Sør-Øst", "Sør-Øst": "Norge"}


def gen_users(num_users: int = 10):
    all_roles = [r for r in WorkerRole]
    for i in range(num_users):
        new_user = schemas.UserCreate(
            name=f"User {i}",
            email=f"user{i}@foo.com",
            phone=1234567890 + i,
            password="password",
            location="Oslo",
            role=all_roles[i % 3],
        )
        create_user(db, new_user)


def gen_regions():
    regions = ["Oslo", "Østlandet", "Sør-Øst", "Norge"]
    regions.reverse()
    for r in regions:
        parent = PARENTS.get(r)
        r_obj = models.Region(
            name=r,
            id=REGION_IDS[r],
            parent_id=REGION_IDS.get(parent),  # type: ignore
        )
        db.add(r_obj)


def gen_companies():
    db.add(
        models.Company(
            name="Oslo University Hospital",
            region_id=REGION_IDS["Oslo"],
            address="123 Somewhere",
            phone=1234567890,
        )
    )
    db.add(
        models.Company(
            name="Rikshospitalet",
            region_id=REGION_IDS["Oslo"],
            address="123 Somewhere Else",
            phone=12345678933,
        )
    )
    db.commit()


def gen_groups():
    db.add(
        models.Group(
            name="Pediatrics",
            company_id=db.query(models.Company)
            .filter(models.Company.name == "Oslo University Hospital")
            .first()
            .id,  # type: ignore
        )
    )
    db.add(
        models.Group(
            name="Cardiology",
            company_id=db.query(models.Company)
            .filter(models.Company.name == "Rikshospitalet")
            .first()
            .id,  # type: ignore
        )
    )


gen_regions()
gen_companies()
gen_groups()
gen_users()
