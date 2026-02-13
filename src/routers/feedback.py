from fastapi import APIRouter, Depends, HTTPException, Path, Request

from src.models import CreateFeedback, Feedback
from src.managers.postgres_manager import PostgresManager
from src import forms
from src.dependencies import CurrentAdminUser, get_postgres_manager

"""Create feedback form management router"""
router = APIRouter()


@router.get("/forms/feedback", response_model=list[Feedback], tags=["forms"])
def get_feedback(
    request: Request,
    current_admin: CurrentAdminUser,
    pg_manager: PostgresManager = Depends(get_postgres_manager),
    ):
    """Get all feedback"""
    if not current_admin.is_admin:
        raise HTTPException(status_code=403)
    return forms.get_all_feedbacks(pg_manager)


@router.post("/forms/feedback", tags=["forms"], status_code=201)
def insert_feedback(
    feedback_data: CreateFeedback,
    request: Request,
    pg_manager: PostgresManager = Depends(get_postgres_manager),
    ):
    """Insert a new feedback"""
    return forms.create_feedback(feedback_data, pg_manager)

@router.put("/forms/feedback/{feedback_id}/archive", tags=["forms"], status_code=201)
def archive_feedback(
    request: Request,
    current_admin: CurrentAdminUser,
    pg_manager: PostgresManager = Depends(get_postgres_manager),
    feedback_id: int = Path(description="The ID of the feedback to archive")
    ):
    """Archive a feedback by its ID"""
    if not current_admin.is_admin:
        raise HTTPException(status_code=403)
    return forms.archive_feedback(feedback_id, pg_manager)