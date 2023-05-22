from fastapi import FastAPI, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from exceptions import *
from database import get_db, engine
from auth.auth_handler import signJWT
from auth.auth_bearer import JWTBearer
import crud, models, schemas

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

# signup
@app.post("/api/signup", tags=["usuario"])
async def create_usuario_signup(usuario: schemas.UsuarioCreate = Body(...), db: Session = Depends(get_db)):
    try:
        crud.create_usuario(db, usuario)
        return signJWT(usuario.usuario)
    except UsuarioException as cie:
        raise HTTPException(**cie.__dict__)
# login
@app.post("/api/login", tags=["usuario"])
async def user_login(usuario: schemas.UsuarioLogin = Body(...), db: Session = Depends(get_db)):
    if crud.check_usuario(db, usuario):
        return signJWT(usuario.usuario)
    raise HTTPException(status_code=400, detail="USUARIO_INCORRETO")

# usuário
@app.get("/api/usuario/{usuario_id}", dependencies=[Depends(JWTBearer())], response_model=schemas.Usuario)
def get_usuario_by_id(usuario_id: int, db: Session = Depends(get_db)):
    try:
        return crud.get_usuario_by_id(db, usuario_id)
    except UsuarioException as cie:
        raise HTTPException(**cie.__dict__)

@app.get("/api/usuario", dependencies=[Depends(JWTBearer())], response_model=schemas.PaginatedUsuario)
def get_all_usuarios(db: Session = Depends(get_db), offset: int = 0, limit: int = 10):
    db_usuarios = crud.get_all_usuarios(db, offset, limit)
    response = {"limit": limit, "offset": offset, "data": db_usuarios}
    return response

@app.post("/api/usuario", dependencies=[Depends(JWTBearer())], response_model=schemas.Usuario)
def create_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_usuario(db, usuario)
    except UsuarioException as cie:
        raise HTTPException(**cie.__dict__)

@app.put("/api/usuario/{usuario_id}", dependencies=[Depends(JWTBearer())], response_model=schemas.Usuario)
def update_usuario(usuario_id: int, usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    try:
        return crud.update_usuario(db, usuario_id, usuario)
    except UsuarioException as cie:
        raise HTTPException(**cie.__dict__)

@app.delete("/api/usuario/{usuario_id}", dependencies=[Depends(JWTBearer())])
def delete_usuario_by_id(usuario_id: int, db: Session = Depends(get_db)):
    try:
        return crud.delete_usuario_by_id(db, usuario_id)
    except UsuarioException as cie:
        raise HTTPException(**cie.__dict__)

# Migracao
@app.get("/api/migracao/{migracao_id}", dependencies=[Depends(JWTBearer())], response_model=schemas.MigracaoDB)
def get_migracao_by_id(migracao_id: int, db: Session = Depends(get_db)):
    try:
        return crud.get_migracao_by_id(db, migracao_id)
    except MigracaoException as cie:
        raise HTTPException(**cie.__dict__)

@app.get("/api/migracao", dependencies=[Depends(JWTBearer())], response_model=schemas.PaginatedMigracao)
def get_all_migracoes(db: Session = Depends(get_db), offset: int = 0, limit: int = 10):
    db_migracoes = crud.get_all_migracoes(db, offset, limit)
    response = {"limit": limit, "offset": offset, "data": db_migracoes}
    return response

@app.post("/api/migracao", dependencies=[Depends(JWTBearer())], response_model=schemas.MigracaoDB)
def create_migracao(migracao: schemas.MigracaoCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_migracacao(db, migracao)
    except MigracaoException as cie:
        raise HTTPException(**cie.__dict__)

@app.put("/api/migracao/{migracao_id}", dependencies=[Depends(JWTBearer())], response_model=schemas.MigracaoDB)
def update_migracao(migracao_id: int, migracao: schemas.MigracaoCreate, db: Session = Depends(get_db)):
    try:
        return crud.update_migracao(db, migracao_id, migracao)
    except MigracaoException as cie:
        raise HTTPException(**cie.__dict__)

@app.delete("/api/migracao/{migracao_id}", dependencies=[Depends(JWTBearer())])
def delete_migracao_by_id(migracao_id: int, db: Session = Depends(get_db)):
    try:
        return crud.delete_migracao_by_id(db, migracao_id)
    except MigracaoException  as cie:
        raise HTTPException(**cie.__dict__)

# Notificacao 
@app.get("/api/notificacao/{notificacao_id}", dependencies=[Depends(JWTBearer())], response_model=schemas.NotificacaoDB)
def get_notificacao_by_id(notificacao_id: int, db: Session = Depends(get_db)):
    try:
        return crud.get_notificacao_by_id(db, notificacao_id)
    except NotificacaoException as cie:
        raise HTTPException(**cie.__dict__)

@app.get("/api/notificacao", dependencies=[Depends(JWTBearer())], response_model=schemas.PaginatedNotificao)
def get_all_notificacoes(db: Session = Depends(get_db), offset: int = 0, limit: int = 10):
    db_notificacoes = crud.get_all_notificacoes(db, offset, limit)
    response = {"limit": limit, "offset": offset, "data": db_notificacoes}
    return response

@app.post("/api/notificacao", dependencies=[Depends(JWTBearer())], response_model=schemas.NotificacaoDB)
def create_notificacao(notificao: schemas.NotificacaoCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_notificacao(db, notificao)
    except NotificacaoException as cie:
        raise HTTPException(**cie.__dict__)

@app.put("/api/notificacao/{notificacao_id}", dependencies=[Depends(JWTBearer())], response_model=schemas.NotificacaoDB)
def update_notificacao(notificacao_id: int, notificacao: schemas.NotificacaoCreate, db: Session = Depends(get_db)):
    try:
        return crud.update_notificacao(db, notificacao_id, notificacao)
    except NotificacaoException as cie:
        raise HTTPException(**cie.__dict__)

@app.delete("/api/notificacao/{notificacao_id}", dependencies=[Depends(JWTBearer())])
def delete_notificacao_by_id(notificacao_id: int, db: Session = Depends(get_db)):
    try:
        return crud.delete_notificao_by_id(db, notificacao_id)
    except NotificacaoException as cie:
        raise HTTPException(**cie.__dict__)

