from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "nse-bs-api"
    PORT: int = 8000
    HOST: str = "0.0.0.0"

    # Risk free rate (annualized). Override via env if needed.
    RISK_FREE: float = 0.065

    # Cache
    REDIS_URL: str | None = None  # e.g., redis://redis:6379/0
    CACHE_TTL_SECONDS: int = 20

    # NSE tuning
    USER_AGENT: str = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    )
    TIMEOUT: int = 15
    RETRIES: int = 3

settings = Settings()
