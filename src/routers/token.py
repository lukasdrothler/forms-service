from fastapi import APIRouter, Depends, Query
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

from src.models import Token
from src.managers.auth_manager import AuthManager
from src.dependencies import get_auth_manager

"""Create token router for authenticated access of forms"""
router = APIRouter()


@router.post("/token", response_model=Token, tags=["tokens"])
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_manager: AuthManager = Depends(get_auth_manager),
    stay_logged_in: bool = Query(False, description="Whether to issue a refresh token")
) -> Token:
    return auth_manager.get_token_for_user(
        username_or_email=form_data.username,
        password=form_data.password,
        stay_logged_in=stay_logged_in
    )