"""FastAPI application entry point"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.db.database import init_db
from app.api import chat, law, conversations
from app.core.exceptions import (
    LawChatException,
    OpenAIAPIError,
    LawNotFoundError,
    ConversationNotFoundError
)
from app.core.error_handlers import (
    lawchat_exception_handler,
    openai_error_handler,
    generic_exception_handler
)
import logging

# 로깅 설정
logging.basicConfig(
    level=logging.INFO if settings.debug else logging.WARNING,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Initialize FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    init_db()
    # NOTE: Using only ASCII characters here to avoid UnicodeEncodeError on Windows cp949 consoles
    print(f"[START] {settings.app_name} v{settings.app_version} started")
    print(f"[ENV] {settings.app_env}")
    print(f"[SERVER] http://{settings.host}:{settings.port}")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


# Include API routers
app.include_router(chat.router)
app.include_router(law.router)
app.include_router(conversations.router)

# 에러 핸들러 등록
app.add_exception_handler(LawChatException, lawchat_exception_handler)
app.add_exception_handler(OpenAIAPIError, openai_error_handler)
app.add_exception_handler(Exception, generic_exception_handler)

