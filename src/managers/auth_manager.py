from fastapi import HTTPException, status

from src.models import User, Token

import os, logging, requests

logger = logging.getLogger(__name__)

class AuthManager:
    def __init__(self):
        if "AUTH_SVC_HOST" in os.environ:
            self.auth_service_host = os.getenv('AUTH_SVC_HOST')
            logger.info(f"Auth service host set to {self.auth_service_host}")
        else:
            raise ValueError("AUTH_SVC_HOST environment variable not set")
        
        if "AUTH_SVC_PORT" in os.environ:
            self.auth_service_port = os.getenv("AUTH_SVC_PORT")
            logger.info(f"Auth service port set to {self.auth_service_port}")
        else:
            raise ValueError("AUTH_SVC_PORT environment variable not set")
        
        if "AUTH_SVC_USER_ENDPOINT" in os.environ:
            self.auth_user_endpoint = os.getenv("AUTH_SVC_USER_ENDPOINT")
        else:
            self.auth_user_endpoint = "/user/me"
        logger.info(f"Auth service user endpoint set to {self.auth_user_endpoint}")
        

        if "AUTH_SVC_TOKEN_ENDPOINT" in os.environ:
            self.auth_token_endpoint = os.getenv("AUTH_SVC_TOKEN_ENDPOINT")
        else:
            self.auth_token_endpoint = "/token" # nosec
        logger.info(f"Auth service token endpoint set to {self.auth_token_endpoint}")
        
        # Ensure the host includes a protocol scheme
        if not self.auth_service_host.startswith(('http://', 'https://')):
            self.auth_service_host = f"http://{self.auth_service_host}"
        
        self.auth_user_url = f"{self.auth_service_host}:{self.auth_service_port}{self.auth_user_endpoint}"
        self.auth_token_url = f"{self.auth_service_host}:{self.auth_service_port}{self.auth_token_endpoint}"


    def _get_error_detail(self, response):
            try:
                error_data = response.json()
                return error_data.get("detail", response.text)
            except:
                return response.text


    def get_token_for_user(self, username_or_email: str, password: str, stay_logged_in: bool = False) -> Token:
        response = requests.post(
            url=self.auth_token_url,
            data={
                "username": username_or_email,
                "password": password,
            },
            params={"stay_logged_in": str(stay_logged_in).lower()},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=10
        )
        
        if response.status_code >= 300:
            raise HTTPException(
                status_code=response.status_code,
                detail=self._get_error_detail(response)
            )
            
        return Token(**response.json())


    def get_user_by_token(self, token: str) -> User:
        response = requests.get(
            url = self.auth_user_url,
            headers={"Authorization": f"Bearer {token}"},
            timeout=10
        )
        if response.status_code >= 300:
            raise HTTPException(
                status_code=response.status_code,
                detail=self._get_error_detail(response)
            )
        response_json = response.json()
        return User(**response_json)


    def get_current_admin_user(self, current_user: User) -> User:
        if not current_user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User does not have admin privileges"
            )
        return current_user