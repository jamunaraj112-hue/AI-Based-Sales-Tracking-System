import os
from pathlib import Path
from dotenv import load_dotenv

# Path resolution using pathlib
APP_DIR = Path(__file__).resolve().parent
BACKEND_DIR = APP_DIR.parent
PROJECT_ROOT = BACKEND_DIR.parent

DATABASE_DIR = PROJECT_ROOT / "database"
FRONTEND_DIR = PROJECT_ROOT / "frontend"
ENV_PATH = PROJECT_ROOT / ".env"

DATABASE_DIR.mkdir(parents=True, exist_ok=True)

if ENV_PATH.exists():
    load_dotenv(ENV_PATH)

class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "SalesTrack AI — Sales Tracking System")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "salestrack-session-secret-key-2026")
    SESSION_COOKIE_NAME: str = "salestrack_session"

    # MySQL Database Settings (Default XAMPP credentials)
    MYSQL_HOST: str = os.getenv("MYSQL_HOST", "127.0.0.1")
    MYSQL_PORT: int = int(os.getenv("MYSQL_PORT", 3306))
    MYSQL_USER: str = os.getenv("MYSQL_USER", "root")
    MYSQL_PASSWORD: str = os.getenv("MYSQL_PASSWORD", "")
    MYSQL_DB: str = os.getenv("MYSQL_DB", "sales_tracking_system")
    
    # MySQL URL for SQLAlchemy
    MYSQL_URL: str = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
    
    # SQLite fallback path
    SQLITE_PATH: Path = DATABASE_DIR / "sales_track.db"
    SQLITE_URL: str = f"sqlite:///{SQLITE_PATH.as_posix()}"

settings = Settings()
