from typing import List
from sqlalchemy.orm import Session
from exceptions import MigracaoNotFoundError, NotificacaoNotFoundError, UsuarioAlreadyExistError, UsuarioNotFoundError 
import bcrypt, models, schemas

# usuário
def check_usuario(db: Session, usuario: schemas.UsuarioLogin):
    db_usuario = get_usuario_by_usuario(db, usuario.usuario) 
    if db_usuario is None:
        return False
    return bcrypt.checkpw(usuario.senha.encode('utf8'), db_usuario.senha.encode('utf8'))

def get_usuarios_by_ids(db: Session, ids: List[int]):
    if (db_usuarios := db.query(models.Usuario).filter(models.Usuario.id.in_(ids))).count() != len(ids):
        raise UsuarioNotFoundError
    return db_usuarios

def get_usuario_by_id(db: Session, usuario_id: int):
    db_usuario = db.query(models.Usuario).get(usuario_id)
    if db_usuario is None:
        raise UsuarioNotFoundError
    return db_usuario

def get_all_usuarios(db: Session, offset: int, limit: int):
    return db.query(models.Usuario).offset(offset).limit(limit).all()

def get_usuario_by_usuario(db: Session, usuario: str):
    return db.query(models.Usuario).filter(models.Usuario.usuario == usuario).first()

def create_usuario(db: Session, usuario: schemas.UsuarioCreate):
    db_usuario = get_usuario_by_usuario(db, usuario.usuario)
    # O parâmetro rounds do gensalt determina a complexidade. O padrão é 12.
    usuario.senha = bcrypt.hashpw(usuario.senha.encode('utf8'), bcrypt.gensalt()).decode('utf8')
    if db_usuario is not None:
        raise UsuarioAlreadyExistError
    db_usuario = models.Usuario(**usuario.dict())
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def update_usuario(db: Session, usuario_id: int, usuario: schemas.UsuarioCreate):
    db_usuario = get_usuario_by_id(db, usuario_id)
    db_usuario_mesmo_usuario = get_usuario_by_usuario(db, usuario.usuario)
    if db_usuario.usuario != usuario.usuario and db_usuario_mesmo_usuario is not None:
        raise UsuarioAlreadyExistError
    db_usuario.nome = usuario.nome
    db_usuario.usuario = usuario.usuario
    if usuario.senha != "":
        # O parâmetro rounds do gensalt determina a complexidade. O padrão é 12.
        db_usuario.senha = bcrypt.hashpw(usuario.senha.encode('utf8'), bcrypt.gensalt())
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def delete_usuario_by_id(db: Session, usuario_id: int):
    db_usuario = get_usuario_by_id(db, usuario_id)
    db.delete(db_usuario)
    db.commit()
    return

# Migracao 
def get_migracao_by_id(db: Session, migracao_id: int):
    db_migracao = db.query(models.Migracao).get(migracao_id)
    if db_migracao is None:
        raise MigracaoNotFoundError 
    return db_migracao

def get_all_migracoes(db: Session, offset: int, limit: int):
    return db.query(models.Migracao).offset(offset).limit(limit).all()

def create_migracacao(db: Session, migracao: schemas.MigracaoCreate):
    db_migracao = models.Migracao(nome=migracao.nome)
    usuarios = get_usuarios_by_ids(db, migracao.usuario_ids)
    db_migracao.usuarios.extend(usuarios)
    db.add(db_migracao)
    db.commit()
    db.refresh(db_migracao)
    return db_migracao

def update_migracao(db: Session, migracao_id: int, migracao: schemas.MigracaoCreate):
    db_migracao = get_migracao_by_id(db, migracao_id)
    db_migracao.nome = migracao.nome
    usuarios = get_usuarios_by_ids(db, migracao.usuario_ids)
    db_migracao.usuarios.extend(usuarios)
    db.commit()
    db.refresh(db_migracao)
    return db_migracao

def delete_migracao_by_id(db: Session, migracao_id: int):
    db_migracao = get_migracao_by_id(db, migracao_id)
    db.delete(db_migracao)
    db.commit()
    return

# Notificao
def get_notificacao_by_id(db: Session, notificacao_id: int):
    db_notificacao = db.query(models.Notificacao).get(notificacao_id) 
    if db_notificacao is None:
        raise NotificacaoNotFoundError
    return db_notificacao

def get_all_notificacoes(db: Session, offset: int, limit: int):
    return db.query(models.Notificacao).offset(offset).limit(limit).all()
   
def create_notificacao(db: Session, notificacao: schemas.NotificacaoCreate):
    get_usuario_by_id(db, notificacao.id_usuario)
    db_notificao = models.Notificacao(id_usuario=notificacao.id_usuario, texto=notificacao.texto)
    db.add(db_notificao)
    db.commit()
    db.refresh(db_notificao)
    return db_notificao

def update_notificacao(db: Session, notificacao_id: int, notificacao: schemas.NotificacaoCreate):
    db_notificacao = get_notificacao_by_id(db, notificacao_id)
    db_notificacao.id_usuario = notificacao.id_usuario 
    db_notificacao.texto = notificacao.texto 
    db.commit()
    db.refresh(db_notificacao)
    return db_notificacao

def delete_notificao_by_id(db: Session, notificao_id: int):
    db_notificao = get_notificacao_by_id(db, notificao_id)
    db.delete(db_notificao)
    db.commit()
    return

