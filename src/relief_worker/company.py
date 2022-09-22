from fastapi import APIRouter

router = APIRouter()


@router.get("/{company_id}")
def view_company(company_id: str):
    ...


@router.post("/{company_id}/edit")
def edit_company():
    ...


@router.get("/{company_id}/shifts")
def view_co_shifts():
    ...


@router.get("/{company_id}/workers")
def view_co_workers():
    ...


@router.get("/{company_id}/groups")
def view_groups(company_id: str):
    ...


@router.get("/{company_id}/groups/{group_id}")
def view_group(company_id: str, group_id: str):
    ...


@router.post("/{company_id}/groups/{group_id}/edit")
def edit_group(company_id: str, group_id: str):
    ...


@router.get("/{company_id}/groups/{group_id}/workers")
def view_group_workers(company_id: str, group_id: str):
    ...


@router.get("/{company_id}/groups/{group_id}/shifts")
def view_group_shifts(company_id: str, group_id: str):
    ...
