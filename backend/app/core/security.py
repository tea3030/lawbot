"""API key management and security utilities"""
from app.core.config import settings


def get_openai_api_key() -> str:
    """Get OpenAI API key from settings"""
    return settings.openai_api_key


def get_law_api_key() -> str:
    """Get Law API key from settings"""
    return settings.law_api_key


