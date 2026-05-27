from sqlalchemy import Column, Integer, String, Date, Numeric, ForeignKey
from config.connection import Base


class Lancamento(Base):
    """
    ORM model for the lancamento table.
    """

    __tablename__ = "lancamento"

    id = Column(Integer, primary_key=True)
    descricao = Column(String)
    data_lancamento = Column(Date)
    valor = Column(Numeric(10, 2))
    tipo_lancamento = Column(String)
    situacao = Column(String)
    id_usuario = Column(Integer, ForeignKey("usuario.id"))
