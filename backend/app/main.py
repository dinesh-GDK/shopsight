"""FastAPI application entry point."""

from fastapi import FastAPI
from app.config import settings
from app.api.routes import router
from app.api.middleware import add_cors_middleware, add_exception_handlers
from app.utils.logger import logger

# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Agentic e-commerce analytics platform with LLM-powered insights",
    debug=settings.DEBUG
)

# Add middleware
add_cors_middleware(app)
add_exception_handlers(app)

# Include routers
app.include_router(router)

# Startup event
@app.on_event("startup")
async def startup_event():
    """Execute on application startup."""
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"Debug mode: {settings.DEBUG}")
    logger.info(f"Ollama host: {settings.OLLAMA_HOST}")
    logger.info(f"Ollama model: {settings.OLLAMA_MODEL}")


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Execute on application shutdown."""
    logger.info(f"Shutting down {settings.APP_NAME}")


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "docs": "/docs"
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.API_RELOAD,
        log_level=settings.LOG_LEVEL.lower()
    )
