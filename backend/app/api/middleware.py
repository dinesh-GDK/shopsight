"""Middleware for FastAPI application."""

from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.utils.exceptions import (
    ShopSightException,
    ProductNotFoundException,
    LLMServiceException,
    DatabaseException
)
from app.utils.logger import logger


def add_cors_middleware(app):
    """
    Add CORS middleware to the application.

    Args:
        app: FastAPI application instance
    """
    from app.config import settings

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    logger.info(f"CORS middleware added with origins: {settings.CORS_ORIGINS}")


def add_exception_handlers(app):
    """
    Add exception handlers to the application.

    Args:
        app: FastAPI application instance
    """

    @app.exception_handler(ProductNotFoundException)
    async def product_not_found_handler(request: Request, exc: ProductNotFoundException):
        """Handle product not found exceptions."""
        logger.warning(f"Product not found: {exc}")
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": "Product not found", "message": str(exc)}
        )

    @app.exception_handler(LLMServiceException)
    async def llm_service_handler(request: Request, exc: LLMServiceException):
        """Handle LLM service exceptions."""
        logger.error(f"LLM service error: {exc}")
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"error": "LLM service unavailable", "message": str(exc)}
        )

    @app.exception_handler(DatabaseException)
    async def database_handler(request: Request, exc: DatabaseException):
        """Handle database exceptions."""
        logger.error(f"Database error: {exc}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": "Database error", "message": str(exc)}
        )

    @app.exception_handler(ShopSightException)
    async def shopsight_exception_handler(request: Request, exc: ShopSightException):
        """Handle general ShopSight exceptions."""
        logger.error(f"ShopSight error: {exc}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": exc.__class__.__name__,
                "message": str(exc)
            }
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """Handle unexpected exceptions."""
        logger.error(f"Unexpected error: {exc}", exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "Internal server error",
                "message": "An unexpected error occurred"
            }
        )

    logger.info("Exception handlers registered")
