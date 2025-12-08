"""Custom exception classes for ShopSight."""


class ShopSightException(Exception):
    """Base exception for ShopSight."""
    pass


class ProductNotFoundException(ShopSightException):
    """Raised when product is not found."""
    pass


class LLMServiceException(ShopSightException):
    """Raised when LLM service fails."""
    pass


class DatabaseException(ShopSightException):
    """Raised when database operation fails."""
    pass


class ValidationException(ShopSightException):
    """Raised when validation fails."""
    pass
