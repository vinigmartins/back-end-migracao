from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import Base

class Usuario(Base):
    __tablename__ = 'usuarios'
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(150))
    usuario = Column(String(80), unique=True, index=True)
    senha = Column(String(255))
    notificacoes = relationship("Notificacao", back_populates="usuario")
    migracoes = relationship("Migracao", secondary="migracao_usuario", back_populates="usuarios")

class Migracao(Base):
    __tablename__ = 'migracoes'
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255))
    usuarios = relationship("Usuario", secondary="migracao_usuario", back_populates="migracoes")

migracao_usuario = Table('migracao_usuario', Base.metadata,
    Column('id_usuario', ForeignKey('usuarios.id'), primary_key=True),
    Column('id_migracao', ForeignKey('migracoes.id'), primary_key=True)
)

class Notificacao(Base):
    __tablename__ = 'notificacoes'

    id = Column(Integer, primary_key=True, index=True)
    texto = Column(String(500))
    id_usuario = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    usuario = relationship("Usuario", back_populates="notificacoes")

