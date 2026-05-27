"""seed data

Revision ID: 975ee4f218ee
Revises: d247904df2b2
Create Date: 2026-05-26 22:28:17.866323

EXECUTA APENAS NA PRIMEIRA VEZ QUE AS MIGRAÇÕES SÃO CRIADAS
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "975ee4f218ee"
down_revision: Union[str, Sequence[str], None] = "d247904df2b2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Seed de usuários
    op.execute(
        "INSERT INTO usuario (nome, login, senha, situacao) VALUES "
        "('Daniel', 'daniel', MD5('123456'), 'ativo'),"
        "('Maria', 'maria', MD5('123456'), 'ativo'),"
        "('Pedro', 'pedro', MD5('123456'), 'ativo')"
    )

    # Seed de lançamentos
    op.execute(
        "INSERT INTO lancamento (descricao, data_lancamento, valor, tipo_lancamento, situacao, id_usuario) VALUES "
        "('Salário', '2024-03-01', 5000.00, 'RECEITA', 'EFETIVADO', 1),"
        "('Aluguel', '2024-03-05', 1200.00, 'DESPESA', 'EFETIVADO', 1),"
        "('Freelance desenvolvimento', '2024-03-08', 1500.00, 'RECEITA', 'PENDENTE', 2),"
        "('Conta de luz', '2024-03-10', 180.50, 'DESPESA', 'EFETIVADO', 2),"
        "('Supermercado', '2024-03-12', 450.75, 'DESPESA', 'EFETIVADO', 1),"
        "('Consultoria', '2024-03-15', 3000.00, 'RECEITA', 'PENDENTE', 3),"
        "('Internet', '2024-03-15', 99.90, 'DESPESA', 'EFETIVADO', 3),"
        "('Venda de equipamento', '2024-03-18', 800.00, 'RECEITA', 'EFETIVADO', 2),"
        "('Plano de saúde', '2024-03-20', 320.00, 'DESPESA', 'PENDENTE', 1),"
        "('Dividendos', '2024-03-25', 2200.00, 'RECEITA', 'EFETIVADO', 3)"
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DELETE FROM lancamento")
    op.execute("DELETE FROM usuario")
