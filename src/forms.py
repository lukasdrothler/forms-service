from src.managers.postgres_manager import PostgresManager
from src.models import CreateCancellation, CreateFeedback, Cancellation, Feedback

from fastapi import HTTPException, status
import logging

logger = logging.getLogger(__name__)

def create_cancellation(cancellation_data: CreateCancellation, pg_manager: PostgresManager):
    """Creates a new cancellation entry in the database."""
    sql = "INSERT INTO cancellation (email, name, last_name, address, town, town_number, is_unordinary, reason, last_invoice_number, termination_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    params = (
        cancellation_data.email,
        cancellation_data.name,
        cancellation_data.last_name,
        cancellation_data.address,
        cancellation_data.town,
        cancellation_data.town_number,
        cancellation_data.is_unordinary,
        cancellation_data.reason,
        cancellation_data.last_invoice_number,
        cancellation_data.termination_date
    )
    try:
        pg_manager.execute_modification_query(sql, params)
    except Exception as e:
        logger.error(f"Error creating cancellation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create cancellation"
        )
    return {"detail": "Cancellation created successfully"}


def create_feedback(feedback_data: CreateFeedback, pg_manager: PostgresManager):
    """Creates a new feedback entry in the database."""
    sql = "INSERT INTO feedback (email, text) VALUES (%s, %s)"
    params = (
        feedback_data.email,
        feedback_data.text
    )
    try:
        pg_manager.execute_modification_query(sql, params)
    except Exception as e:
        logger.error(f"Error creating feedback: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create feedback"
        )
    return {"detail": "Feedback created successfully"}


def archive_cancellation(cancellation_id: int, pg_manager: PostgresManager):
    """Archive a cancellation entry in the database."""
    sql = "UPDATE cancellation SET is_archived = true WHERE id = %s"
    params = (cancellation_id,)
    try:
        pg_manager.execute_modification_query(sql, params)
    except Exception as e:
        logger.error(f"Error archiving cancellation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to archive cancellation"
        )
    return {"detail": "Cancellation archived successfully"}


def archive_feedback(feedback_id: int, pg_manager: PostgresManager):
    """Archive a feedback entry in the database."""
    sql = "UPDATE feedback SET is_archived = true WHERE id = %s"
    params = (feedback_id,)
    try:
        pg_manager.execute_modification_query(sql, params)
    except Exception as e:
        logger.error(f"Error archiving feedback: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to archive feedback"
        )
    return {"detail": "Feedback archived successfully"}


def get_all_cancellations(pg_manager: PostgresManager) -> list[Feedback]:
    """Retrieve all cancellations from the database."""
    sql = "SELECT * FROM cancellation"
    try:
        cancellations = pg_manager.execute_query(sql)
    except Exception as e:
        logger.error(f"Error retrieving cancellations: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve cancellations"
        )
    return [Cancellation(**cancellation) for cancellation in cancellations]


def get_all_feedbacks(pg_manager: PostgresManager) -> list[Feedback]:
    """Retrieve all feedbacks from the database."""
    sql = "SELECT * FROM feedback"
    try:
        feedbacks = pg_manager.execute_query(sql)
    except Exception as e:
        logger.error(f"Error retrieving feedbacks: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve feedbacks"
        )
    return [Feedback(**feedback) for feedback in feedbacks]