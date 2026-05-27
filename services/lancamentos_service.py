from sqlalchemy.exc import SQLAlchemyError
from config.connection import SessionLocal
from models.lancamento import Lancamento


def listar_lancamentos(id_usuario=None, data_filtro=None, situacao_filtro=None):
    """
    Access the database and list the launches with optional filters.
    """
    with SessionLocal() as db:
        try:
            query = db.query(Lancamento)

            if id_usuario:
                query = query.filter(Lancamento.id_usuario == id_usuario)
            if data_filtro:
                query = query.filter(Lancamento.data_lancamento == data_filtro)
            if situacao_filtro and situacao_filtro != "ALL":
                query = query.filter(Lancamento.situacao == situacao_filtro)

            query = query.order_by(Lancamento.data_lancamento.desc())

            lancamentos = query.all()
            return [
                {
                    "id": l.id,
                    "descricao": l.descricao,
                    "data_lancamento": l.data_lancamento,
                    "valor": l.valor,
                    "tipo_lancamento": l.tipo_lancamento,
                    "situacao": l.situacao,
                    "id_usuario": l.id_usuario,
                }
                for l in lancamentos
            ]
        except SQLAlchemyError as e:
            print(f"Erro ao buscar lançamentos: {e}")
            return []


def inserir_lancamento(
    *,
    descricao,
    data_lancamento,
    valor,
    tipo_lancamento,
    situacao,
    id_usuario,
):
    """
    Inserts a new launch into the database.
    """
    with SessionLocal() as db:
        try:
            lancamento = Lancamento(
                descricao=descricao,
                valor=valor,
                data_lancamento=data_lancamento,
                situacao=situacao,
                tipo_lancamento=tipo_lancamento,
                id_usuario=id_usuario,
            )
            db.add(lancamento)
            db.commit()
            return True
        except SQLAlchemyError as e:
            db.rollback()
            print(f"Erro ao inserir lançamento: {e}")
            return False


def buscar_lancamento_por_id(launch_id):
    """
    Finds a specific launch by its ID.
    """
    with SessionLocal() as db:
        try:
            lancamento = db.query(Lancamento).filter(Lancamento.id == launch_id).first()
            if lancamento:
                return {
                    "id": lancamento.id,
                    "descricao": lancamento.descricao,
                    "data_lancamento": lancamento.data_lancamento,
                    "valor": lancamento.valor,
                    "tipo_lancamento": lancamento.tipo_lancamento,
                    "situacao": lancamento.situacao,
                    "id_usuario": lancamento.id_usuario,
                }
            return None
        except SQLAlchemyError as e:
            print(f"Erro ao buscar lançamento por id: {e}")
            return None


def atualizar_lancamento(
    *,
    launch_id,
    descricao,
    data_lancamento,
    valor,
    tipo_lancamento,
    situacao,
    id_usuario,
):
    """
    Updates the data of an existing launch.
    """
    with SessionLocal() as db:
        try:
            db.query(Lancamento).filter(Lancamento.id == launch_id).update(
                {
                    "descricao": descricao,
                    "data_lancamento": data_lancamento,
                    "valor": valor,
                    "tipo_lancamento": tipo_lancamento,
                    "situacao": situacao,
                    "id_usuario": id_usuario,
                }
            )
            db.commit()
            return True
        except SQLAlchemyError as e:
            db.rollback()
            print(f"Erro ao atualizar lançamento: {e}")
            return False


def deletar_lancamento_db(launch_id):
    """
    Deletes a launch from the database.
    """
    with SessionLocal() as db:
        try:
            db.query(Lancamento).filter(Lancamento.id == launch_id).delete()
            db.commit()
            return True
        except SQLAlchemyError as e:
            db.rollback()
            print(f"Erro ao deletar lançamento: {e}")
            return False
