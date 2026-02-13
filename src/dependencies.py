"""
Dependency injection container for FastAPI Utils
"""
from typing import Any, Dict, Callable

from src.managers.postgres_manager import PostgresManager


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


def setup_dependencies() -> None:
    """Setup all dependencies in the container"""
    container.clear()
    
    # Register singleton instances
    container.register_singleton("postgres_manager", create_postgres_manager())


def get_postgres_manager() -> PostgresManager:
    """FastAPI dependency function to get PostgresManager instance"""
    return container.get("postgres_manager")