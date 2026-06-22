from sqlalchemy import Column, Integer, String
from config.connection import Base


class Teste2(Base):
    """
    ORM model for the teste2 table.
    """

    __tablename__ = "teste2"

    id = Column(Integer, primary_key=True)
    descricao = Column(String)
