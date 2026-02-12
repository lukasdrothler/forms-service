"""
Dependency injection container for FastAPI Utils
"""
from typing import Annotated, Any, Dict, Callable

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from src.models import User
from src.managers.postgres_manager import PostgresManager
from src.managers.auth_manager import AuthManager


class DependencyContainer:
    """Dependency injection container for managing service instances"""
    
    def __init__(self):
        self._factories: Dict[str, Callable] = {}
        self._singletons: Dict[str, Any] = {}
        
    def register_singleton(self, service_name: str, instance: Any) -> None:
        """Register a singleton service instance"""
        self._singletons[service_name] = instance
        
    def register_factory(self, service_name: str, factory: Callable) -> None:
        """Register a factory function for creating service instances"""
        self._factories[service_name] = factory
        
    def get(self, service_name: str) -> Any:
        """Get a service instance"""
        # Check if it's a singleton first
        if service_name in self._singletons:
            return self._singletons[service_name]
            
        # Check if there's a factory for it
        if service_name in self._factories:
            instance = self._factories[service_name]()
            # Cache as singleton after first creation
            self._singletons[service_name] = instance
            return instance
            
        raise ValueError(f"Service '{service_name}' not found in container")
    
    def clear(self) -> None:
        """Clear all registered services"""
        self._factories.clear()
        self._singletons.clear()


# Global dependency container instance
container = DependencyContainer()


def create_postgres_manager() -> PostgresManager:
    """Factory function to create PostgresManager instance"""
    return PostgresManager()


def create_auth_manager() -> AuthManager:
    """Factory function to create AuthManager instance"""
    return AuthManager()


def setup_dependencies() -> None:
    """Setup all dependencies in the container"""
    container.clear()
    
    # Register singleton instances
    container.register_singleton("postgres_manager", create_postgres_manager())
    container.register_singleton("auth_manager", create_auth_manager())


def get_postgres_manager() -> PostgresManager:
    """FastAPI dependency function to get PostgresManager instance"""
    return container.get("postgres_manager")


def get_auth_manager() -> AuthManager:
    """FastAPI dependency function to get AuthManager instance"""
    return container.get("auth_manager")


# OAuth2 scheme for extracting bearer tokens from Authorization header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_bearer_token(token: Annotated[str, Depends(oauth2_scheme)]) -> str:
    """FastAPI dependency function to extract bearer token from Authorization header"""
    return token


# Convenience type annotation for bearer token - use this in route handlers
BearerToken = Annotated[str, Depends(get_bearer_token)]

def get_current_user(
    token: BearerToken,
    auth_manager: AuthManager = Depends(get_auth_manager)
) -> User:
    """FastAPI dependency to validate token and get current user"""
    return auth_manager.get_user_by_token(token)


def get_current_admin_user(
    current_user: Annotated[User, Depends(get_current_user)],
    auth_manager: AuthManager = Depends(get_auth_manager)
) -> User:
    """Dependency to get current admin user"""
    return auth_manager.get_current_admin_user(current_user)

# Convenience type annotation
CurrentAdminUser = Annotated[User, Depends(get_current_admin_user)]
