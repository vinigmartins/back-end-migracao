from typing import List  
from pydantic import BaseModel

# todo Remover Base do nome
class UsuarioBase(BaseModel):
    nome: str
    usuario: str
class UsuarioCreate(UsuarioBase):
    senha: str
class Usuario(UsuarioBase):
    id: int
    class Config:
        orm_mode = True
class UsuarioLogin(BaseModel):
    usuario: str
    senha: str
    class Config:
        schema_extra = {
            "example": {
                "usuario": "user.name",
                "senha": "pass"
            }
        }
class PaginatedUsuario(BaseModel):
    limit: int
    offset: int
    data: List[Usuario]

class Migracao(BaseModel):
    nome: str
    
class MigracaoCreate(Migracao):
    usuario_ids: List[int] = []
    
class MigracaoDB(Migracao):
    id: int
    usuarios: List[Usuario] = [] 
    class Config:
        orm_mode = True
        
class PaginatedMigracao(BaseModel):
    limit: int
    offset: int
    data: List[MigracaoDB]

class Notificacao(BaseModel):
    id_usuario: int
    texto: str 

class NotificacaoCreate(Notificacao):
    pass

class NotificacaoDB(Notificacao):
    id: int
    class Config:
        orm_mode = True

class PaginatedNotificao(BaseModel):
    limit: int
    offset: int
    data: List[NotificacaoDB]

