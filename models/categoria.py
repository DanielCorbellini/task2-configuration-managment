from sqlalchemy import Column, Integer, String
from config.connection import Base


class Categoria(Base):
    """
    ORM model for the categoria table.
    """

    __tablename__ = "categoria"

    id = Column(Integer, primary_key=True)
    descricao = Column(String)
