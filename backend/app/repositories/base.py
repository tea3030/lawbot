"""Base repository interface for database abstraction"""
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, List
from datetime import datetime

T = TypeVar('T')
ID = TypeVar('ID')


class BaseRepository(ABC, Generic[T, ID]):
    """Base repository interface"""
    
    @abstractmethod
    async def create(self, entity: T) -> T:
        """Create a new entity"""
        pass
    
    @abstractmethod
    async def get_by_id(self, id: ID) -> Optional[T]:
        """Get entity by ID"""
        pass
    
    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        """Get all entities with pagination"""
        pass
    
    @abstractmethod
    async def update(self, id: ID, entity: T) -> Optional[T]:
        """Update entity"""
        pass
    
    @abstractmethod
    async def delete(self, id: ID) -> bool:
        """Delete entity"""
        pass


