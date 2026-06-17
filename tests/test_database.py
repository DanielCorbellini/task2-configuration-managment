import pytest
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from config.connection import engine


def test_real_db_connection_success():
    """
    Tests if the application can successfully establish a live connection to the PostgreSQL
    database.
    This test runs completely independently of the `mock_db_connection` fixture.
    """
    try:
        with engine.connect() as conn:
            # Executes an extremely simple ping operation against the database
            result = conn.execute(text("SELECT 1"))
            row = result.fetchone()
            assert row[0] == 1
    except SQLAlchemyError as e:
        pytest.fail(f"Erro na conexão com o banco de dados: {e}")
