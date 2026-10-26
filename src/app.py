import os
import uvicorn

from contextlib import asynccontextmanager

# ==================== FASTAPI IMPORTS ====================
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from routers.room_router import router
from dtos.api_response_dto import APIResponse, Error
from dtos.custom_app_exception import CustomAppException
from errors.error_codes import ErrorCode, ErrorCodeStatus
from constants.http_status import HttpStatusCode
from migrations.migration import Migration
from config.config_manager import *
# ==================== LIFESPAN EVENTS ====================
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    migration = Migration()
    migration.run_startup_migration()

    
    yield
    # Shutdown (if needed)

# ==================== FASTAPI APPLICATION INITIALIZATION ====================
app = FastAPI(
    title="AI Room Suggestion API",
    description="RA-based intelligent room booking and suggestion system",
    version="1.0.0",
    lifespan=lifespan
)

# SQ_1.18 to 1.19 fetch_groups
# ==================== MIDDLEWARE CONFIGURATION ====================
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        origin.strip()
        for origin in os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
        if origin.strip()
    ],
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)

app.include_router(router)

# ==================== EXCEPTION HANDLERS ====================
@app.exception_handler(CustomAppException)
async def custom_exception_handler(request: Request, exc: CustomAppException):
    api_response = exc.to_api_response()
    return JSONResponse(
        status_code=exc.status_code,
        content=api_response.to_dict()
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for error in exc.errors():
        errors.append(Error(
            code=ErrorCode.VALIDATION_ERROR,
            message=f"{error['loc'][-1]}: {error['msg']}",
            error_code_id=ErrorCodeStatus[ErrorCode.VALIDATION_ERROR]
        ))
    
    api_response = APIResponse(
        data=None,
        errors=errors,
        code=HttpStatusCode.UNPROCESSABLE_ENTITY
    )
    
    return JSONResponse(
        status_code=HttpStatusCode.UNPROCESSABLE_ENTITY,
        content=api_response.to_dict()
    )

# ==================== APPLICATION ENTRY POINT ====================
if __name__ == "__main__":
    """
    Main entry point for running the FastAPI application locally.
    """
    uvicorn.run(
        "app:app",
        host=config.host,
        port=config.port,
        reload=os.getenv("RELOAD", "false").lower() == "true",
        log_level="info"
    )
