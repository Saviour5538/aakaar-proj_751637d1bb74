import os
from datetime import datetime
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from database.config import get_db, Base
from backend.routes.auth import router as auth_router
from backend.routes.todos import router as todos_router

# FastAPI application setup
app = FastAPI(
    title="TodoApp",
    description="A Todo application with AI features",
    version="1.0.0",
)

# CORS middleware setup
origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Lifespan context manager for startup/shutdown
@app.on_event("startup")
async def startup_event():
    # Initialize database
    try:
        db = get_db()
        Base.metadata.create_all(bind=db.get_bind())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database initialization failed: {str(e)}")

@app.on_event("shutdown")
async def shutdown_event():
    # Perform any necessary cleanup
    pass

# Global exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()},
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred."},
    )

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}

# Include routers
app.include_router(auth_router, prefix="/api")
app.include_router(todos_router, prefix="/api")