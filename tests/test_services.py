from unittest.mock import MagicMock
from services.usuario_service import autenticar_usuario, listar_usuarios
from services.lancamentos_service import (
    listar_lancamentos,
    inserir_lancamento,
    buscar_lancamento_por_id,
    atualizar_lancamento,
    deletar_lancamento_db,
)


def test_autenticar_usuario_valid(mock_db_connection):
    """
    Test authentication of valid user.
    """
    mock_usuario = MagicMock()
    mock_usuario.id = 1
    mock_usuario.nome = "admin"
    mock_usuario.login = "admin"
    mock_usuario.situacao = "ATIVO"
    # MD5 de "123"
    mock_usuario.senha = "202cb962ac59075b964b07152d234b70"

    mock_query = MagicMock()
    mock_query.filter.return_value.first.return_value = mock_usuario
    mock_db_connection.query.return_value = mock_query

    result = autenticar_usuario("admin", "123")
    assert result is not None
    assert result["id"] == 1


def test_autenticar_usuario_invalid(mock_db_connection):
    """
    Test authentication of invalid user.
    """
    mock_query = MagicMock()
    mock_query.filter.return_value.first.return_value = None
    mock_db_connection.query.return_value = mock_query

    result = autenticar_usuario("admin", "wrong")
    assert result is None


def test_listar_usuarios(mock_db_connection):
    """
    Test listing users.
    """
    mock_usuario = MagicMock()
    mock_usuario.id = 1
    mock_usuario.nome = "A"

    mock_db_connection.query.return_value.all.return_value = [mock_usuario]

    result = listar_usuarios()
    assert len(result) == 1


def test_listar_lancamentos_filters(mock_db_connection):
    """
    Test listing launches with filters.
    """
    mock_query = MagicMock()
    mock_query.filter.return_value = mock_query
    mock_query.order_by.return_value = mock_query
    mock_query.all.return_value = []
    mock_db_connection.query.return_value = mock_query

    result = listar_lancamentos(
        id_usuario=1, data_filtro="2024-01-01", situacao_filtro="EFETIVADO"
    )

    assert result == []
    assert mock_db_connection.query.called


def test_inserir_lancamento(mock_db_connection):
    """
    Test inserting a launch.
    """
    result = inserir_lancamento(
        descricao="Desc",
        data_lancamento="2024-01-01",
        valor=10,
        tipo_lancamento="DESPESA",
        situacao="PENDENTE",
        id_usuario=1,
    )

    assert result is True
    assert mock_db_connection.add.called
    assert mock_db_connection.commit.called


def test_buscar_lancamento_por_id(mock_db_connection):
    """
    Test finding a launch by ID.
    """
    mock_lancamento = MagicMock()
    mock_lancamento.id = 5
    mock_lancamento.descricao = "Test"
    mock_lancamento.data_lancamento = "2024-01-01"
    mock_lancamento.valor = 100
    mock_lancamento.tipo_lancamento = "RECEITA"
    mock_lancamento.situacao = "EFETIVADO"
    mock_lancamento.id_usuario = 1

    mock_query = MagicMock()
    mock_query.filter.return_value.first.return_value = mock_lancamento
    mock_db_connection.query.return_value = mock_query

    result = buscar_lancamento_por_id(5)
    assert result is not None
    assert result["id"] == 5


def test_atualizar_lancamento(mock_db_connection):
    """
    Test updating a launch.
    """
    mock_query = MagicMock()
    mock_query.filter.return_value.update.return_value = 1
    mock_db_connection.query.return_value = mock_query

    result = atualizar_lancamento(
        launch_id=1,
        descricao="D",
        data_lancamento="2024-01-01",
        valor=5,
        tipo_lancamento="RECEITA",
        situacao="PENDENTE",
        id_usuario=1,
    )

    assert result is True
    assert mock_db_connection.commit.called


def test_deletar_lancamento_db(mock_db_connection):
    """
    Test deleting a launch.
    """
    mock_query = MagicMock()
    mock_query.filter.return_value.delete.return_value = 1
    mock_db_connection.query.return_value = mock_query

    result = deletar_lancamento_db(1)

    assert result is True
    assert mock_db_connection.commit.called
