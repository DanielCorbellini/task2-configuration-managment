import hashlib
from sqlalchemy.exc import SQLAlchemyError
from config.connection import SessionLocal
from models.usuario import Usuario


def buscar_usuario_por_login(login):
    """
    Searches for a user in the database by their login.
    """
    with SessionLocal() as db:
        try:
            usuario = db.query(Usuario).filter(Usuario.login == login).first()
            if usuario:
                return {
                    "id": usuario.id,
                    "nome": usuario.nome,
                    "login": usuario.login,
                    "situacao": usuario.situacao,
                }
            return None
        except SQLAlchemyError as e:
            print(f"Erro ao buscar usuário: {e}")
            return None


def listar_usuarios():
    """
    Lists all users in the database.
    """
    with SessionLocal() as db:
        try:
            usuarios = db.query(Usuario).all()
            return [{"id": u.id, "nome": u.nome} for u in usuarios]
        except SQLAlchemyError as e:
            print(f"Erro ao listar usuários: {e}")
            return []


def autenticar_usuario(login, senha):
    """
    Checks the user credentials.
    Generates the MD5 hash of the provided password and compares it
    with the password registered in the database.
    """
    with SessionLocal() as db:
        try:
            usuario = db.query(Usuario).filter(Usuario.login == login).first()

            if usuario:
                senha_hash = hashlib.md5(senha.encode("utf-8")).hexdigest()

                if usuario.senha == senha_hash:
                    return {
                        "id": usuario.id,
                        "nome": usuario.nome,
                        "login": usuario.login,
                        "situacao": usuario.situacao,
                    }

            return None
        except SQLAlchemyError as e:
            print(f"Erro ao autenticar usuário: {e}")
            return None
