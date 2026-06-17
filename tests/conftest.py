from unittest.mock import MagicMock
import pytest
from app import app as flask_app


@pytest.fixture
def app():
    """
    Configures the Flask application for testing
    """
    flask_app.config.update({"TESTING": True, "SECRET_KEY": "test_secret_key"})
    yield flask_app


@pytest.fixture
# pylint: disable-next=redefined-outer-name
def client(app):
    """
    Creates a test client
    """
    return app.test_client()


@pytest.fixture
def mock_db_connection(mocker):
    """
    Mocks the SQLAlchemy SessionLocal used by all services.
    Supports usage as: with SessionLocal() as db: ...
    """
    mock_session = MagicMock()

    # SessionLocal() retorna mock_session; suporte ao context manager (with ... as db)
    mock_session_local = MagicMock(return_value=mock_session)
    mock_session.__enter__ = MagicMock(return_value=mock_session)
    mock_session.__exit__ = MagicMock(return_value=False)

    mocker.patch("services.lancamentos_service.SessionLocal", mock_session_local)
    mocker.patch("services.usuario_service.SessionLocal", mock_session_local)

    return mock_session
