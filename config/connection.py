# pylint: disable=invalid-name
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

Base = declarative_base()


def _get_database_url():
    """Builds the database URL from environment variables."""
    return (
        f"postgresql+psycopg2://"
        f"{os.getenv('DB_USER', 'postgres')}:"
        f"{os.getenv('DB_PASSWORD', 'postgres')}@"
        f"{os.getenv('DB_HOST', 'localhost')}:"
        f"{os.getenv('DB_PORT', '5432')}/"
        f"{os.getenv('DB_NAME', 'postgres')}"
    )


# Container mutável: modificar o conteúdo de um dict não requer `global`
_cache: dict = {"engine": None, "session_factory": None}


def get_engine():
    """Returns the SQLAlchemy engine, creating it on first use."""
    if _cache["engine"] is None:
        _cache["engine"] = create_engine(_get_database_url())
    return _cache["engine"]


def get_session_factory():
    """Returns the session factory, creating it on first use."""
    if _cache["session_factory"] is None:
        _cache["session_factory"] = sessionmaker(
            autocommit=False, autoflush=False, bind=get_engine()
        )
    return _cache["session_factory"]


# Mantém compatibilidade com código que importa SessionLocal diretamente
class _LazySessionLocal:
    """Proxy that creates the real SessionLocal only when first called."""

    def __call__(self, *args, **kwargs):
        return get_session_factory()

    def __getattr__(self, item):
        return getattr(get_session_factory(), item)


SessionLocal = _LazySessionLocal()


def get_db():
    """
    Dependency to get a database session.
    """
    db = get_session_factory()
    try:
        yield db
    finally:
        db.close()
