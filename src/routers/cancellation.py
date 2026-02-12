from fastapi import APIRouter, Depends, HTTPException, Path, Request

from src.models import Cancellation, CreateCancellation
from src.managers.postgres_manager import PostgresManager
from src import forms
from src.dependencies import CurrentAdminUser, get_postgres_manager

"""Create cancellation form management router"""
router = APIRouter()

@router.get("/forms/cancellation", response_model=list[Cancellation], tags=["forms"])
def get_cancellation(
    request: Request,
    current_admin: CurrentAdminUser,
    pg_manager: PostgresManager = Depends(get_postgres_manager),
    ):
    """Get all cancellations"""
    if not current_admin.is_admin:
        raise HTTPException(status_code=403)
    return forms.get_all_cancellations(pg_manager)


@router.post("/forms/cancellation", tags=["forms"], status_code=201)
def insert_cancellation(
    cancellation_data: CreateCancellation,
    request: Request,
    pg_manager: PostgresManager = Depends(get_postgres_manager),
    ):
    """Insert a new cancellation"""
    return forms.create_cancellation(cancellation_data, pg_manager)


@router.patch("/forms/cancellation/{cancellation_id}/archive", tags=["forms"], status_code=201)
def archive_cancellation(
    request: Request,
    current_admin: CurrentAdminUser,
    pg_manager: PostgresManager = Depends(get_postgres_manager),
    cancellation_id: int = Path(description="The ID of the cancellation to archive")
    ):
    """Archive a cancellation by its ID"""
    if not current_admin.is_admin:
        raise HTTPException(status_code=403)
    return forms.archive_cancellation(cancellation_id, pg_manager)
