import pymysql
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import settings

Base = declarative_base()

def initialize_database():
    """Attempts MySQL (XAMPP) connection first, creates DB if missing, or falls back to SQLite."""
    try:
        # Check MySQL server connection
        conn = pymysql.connect(
            host=settings.MYSQL_HOST,
            user=settings.MYSQL_USER,
            password=settings.MYSQL_PASSWORD,
            port=settings.MYSQL_PORT,
            connect_timeout=2
        )
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{settings.MYSQL_DB}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        conn.commit()
        cursor.close()
        conn.close()

        engine = create_engine(settings.MYSQL_URL, pool_pre_ping=True)
        print(f"[DATABASE] Connected successfully to MySQL: '{settings.MYSQL_DB}'")
        return engine, "mysql"
    except Exception as err:
        print(f"[DATABASE] MySQL server not running on localhost:3306 ({err}).")
        print(f"[DATABASE] Using local SQLite database at: {settings.SQLITE_PATH}")
        engine = create_engine(settings.SQLITE_URL, connect_args={"check_same_thread": False})
        return engine, "sqlite"

engine, DB_TYPE = initialize_database()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Provides a transactional database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
