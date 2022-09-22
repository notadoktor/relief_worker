from fastapi import APIRouter

from relief_worker import models, schemas

router = APIRouter()


@router.get("/{company_id}", response_model=schemas.Company)
def view_company(company_id: str):
    ...


@router.post("/{company_id}/edit", response_model=schemas.Company)
def edit_company():
    ...


@router.get("/{company_id}/workers", response_model=list[schemas.User])
def view_co_workers():
    ...


@router.get("/{company_id}/groups", response_model=list[schemas.Group])
def view_groups(company_id: str):
    ...


@router.get("/{company_id}/groups/{group_id}", response_model=schemas.Group)
def view_group(company_id: str, group_id: str):
    ...


@router.post("/{company_id}/groups/{group_id}/edit", response_model=schemas.Group)
def edit_group(company_id: str, group_id: str):
    ...


@router.get("/{company_id}/groups/{group_id}/workers", response_model=list[schemas.User])
def view_group_workers(company_id: str, group_id: str):
    ...


@router.get("/{company_id}/groups/{group_id}/shifts", response_model=list[schemas.Shift])
def view_group_shifts(company_id: str, group_id: str):
    ...
