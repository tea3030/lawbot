"""Application configuration with environment variable validation"""
from typing import List, Literal
import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator


class Settings(BaseSettings):
    """Application settings with validation"""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # OpenAI API
    openai_api_key: str = Field(..., description="OpenAI API key")
    
    # 법령 API (국가법령정보센터)
    law_api_key: str = Field(default="", description="Law API key")
    
    # 애플리케이션 설정
    app_env: str = Field(default="development", description="Application environment")
    app_name: str = Field(default="LawChat", description="Application name")
    app_version: str = Field(default="1.0.0", description="Application version")
    
    # 시간대 설정
    timezone: str = Field(default="Asia/Seoul", description="Application timezone")
    default_timezone: str = Field(default="UTC", description="Default timezone for storage")
    
    # 데이터베이스 설정
    db_type: Literal["sqlite", "firestore"] = Field(
        default="sqlite",
        description="Database type: sqlite (local) or firestore (Firebase)"
    )
    database_url: str = Field(default="sqlite:///./lawchat.db", description="Database URL (SQLite only)")
    
    # Firebase 설정 (Firestore 사용 시)
    firebase_project_id: str = Field(default="", description="Firebase project ID")
    firebase_credentials_path: str = Field(default="", description="Path to Firebase service account JSON")
    
    # 서버 설정
    host: str = Field(default="0.0.0.0", description="Server host")
    port: int = Field(default=8000, description="Server port")
    debug: bool = Field(default=True, description="Debug mode")
    
    # CORS 설정
    cors_origins: str = Field(
        default="http://localhost:5173,http://localhost:3000",
        description="CORS allowed origins (comma-separated)"
    )
    
    @field_validator("openai_api_key")
    @classmethod
    def validate_openai_key(cls, v: str) -> str:
        """Validate OpenAI API key is provided"""
        if not v or v == "your_openai_api_key_here":
            raise ValueError("OPENAI_API_KEY must be set in environment variables")
        return v
    
    @field_validator("firebase_project_id")
    @classmethod
    def validate_firebase_config(cls, v: str, info) -> str:
        """Validate Firebase config when using Firestore"""
        if info.data.get("db_type") == "firestore":
            if not v:
                raise ValueError("FIREBASE_PROJECT_ID is required when DB_TYPE=firestore")
        return v
    
    @field_validator("firebase_credentials_path")
    @classmethod
    def validate_firebase_credentials(cls, v: str, info) -> str:
        """Validate Firebase credentials path when using Firestore"""
        if info.data.get("db_type") == "firestore":
            if not v:
                raise ValueError("FIREBASE_CREDENTIALS_PATH is required when DB_TYPE=firestore")
            if not os.path.exists(v):
                raise FileNotFoundError(f"Firebase credentials file not found: {v}")
        return v
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Get CORS origins as a list"""
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]
    
    @property
    def is_firestore(self) -> bool:
        """Check if using Firestore"""
        return self.db_type == "firestore"
    
    @property
    def is_sqlite(self) -> bool:
        """Check if using SQLite"""
        return self.db_type == "sqlite"


def get_settings() -> Settings:
    """Get application settings with validation"""
    try:
        return Settings()
    except Exception as e:
        raise RuntimeError(
            f"Failed to load settings. Please check your .env file. Error: {e}"
        ) from e


# Global settings instance
settings = get_settings()
