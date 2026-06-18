from sqlalchemy import Column, Integer, String
from config.connection import Base


class Teste(Base):
    """
    ORM model for the teste table.
    """

    __tablename__ = "teste"

    id = Column(Integer, primary_key=True)
    descricao = Column(String)
