"""
CypherGuy Backend Configuration

This module contains all configuration settings for the CypherGuy backend.
"""

import os
from typing import Optional

class Settings:
    """Application settings"""
    
    # API Settings
    API_TITLE: str = "CypherGuy API"
    API_VERSION: str = "0.1.0"
    API_DESCRIPTION: str = "Personal DeFi Assistant API"
    
    # Server Settings
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # Solana Settings
    SOLANA_RPC_URL: str = os.getenv("SOLANA_RPC_URL", "https://api.devnet.solana.com")
    SOLANA_WS_URL: str = os.getenv("SOLANA_WS_URL", "wss://api.devnet.solana.com")
    SOLANA_COMMITMENT: str = os.getenv("SOLANA_COMMITMENT", "confirmed")
    
    # Arcium Settings (Mock for now)
    ARCIUM_API_URL: str = os.getenv("ARCIUM_API_URL", "https://api.arcium.com")
    ARCIUM_API_KEY: Optional[str] = os.getenv("ARCIUM_API_KEY")
    
    # Tangem Settings (Mock for now)
    TANGEM_API_URL: str = os.getenv("TANGEM_API_URL", "https://api.tangem.com")
    TANGEM_API_KEY: Optional[str] = os.getenv("TANGEM_API_KEY")
    
    # Agent Settings
    AGENT_TIMEOUT: int = int(os.getenv("AGENT_TIMEOUT", "30"))
    AGENT_RETRY_ATTEMPTS: int = int(os.getenv("AGENT_RETRY_ATTEMPTS", "3"))
    
    # Security Settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "cypherguy-secret-key-change-in-production")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # Logging Settings
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Database Settings (if needed)
    DATABASE_URL: Optional[str] = os.getenv("DATABASE_URL")
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = int(os.getenv("RATE_LIMIT_REQUESTS", "100"))
    RATE_LIMIT_WINDOW: int = int(os.getenv("RATE_LIMIT_WINDOW", "60"))  # seconds
    
    # Feature Flags
    ENABLE_ARCUM: bool = os.getenv("ENABLE_ARCUM", "False").lower() == "true"
    ENABLE_TANGEM: bool = os.getenv("ENABLE_TANGEM", "False").lower() == "true"
    ENABLE_REAL_SOLANA: bool = os.getenv("ENABLE_REAL_SOLANA", "False").lower() == "true"
    
    # Mock Settings
    MOCK_CREDIT_LIMIT: float = float(os.getenv("MOCK_CREDIT_LIMIT", "10000"))
    MOCK_CREDIT_RATE: float = float(os.getenv("MOCK_CREDIT_RATE", "8.5"))
    MOCK_TRADE_LIMIT: float = float(os.getenv("MOCK_TRADE_LIMIT", "50000"))

# Global settings instance
settings = Settings()
