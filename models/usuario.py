from sqlalchemy import Column, Integer, String
from config.connection import Base


class Usuario(Base):
    """
    ORM model for the usuario table.
    """

    __tablename__ = "usuario"

    id = Column(Integer, primary_key=True)
    nome = Column(String)
    login = Column(String)
    senha = Column(String)
    situacao = Column(String)
