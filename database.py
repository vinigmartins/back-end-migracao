from sqlalchemy import create_engine 
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import sessionmaker
from decouple import config

SGBD = str(config("sgbd"))
CLIENT_DATABASE = str(config("client_database"))
HOST = str(config("host"))
PORT = str(config("port"))
DATABASE = str(config("database"))
USER = str(config("user"))
PASS= str(config("password"))

engine = create_engine(f'{SGBD}+{CLIENT_DATABASE}://{USER}:{PASS}@{HOST}:{PORT}/{DATABASE}')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)  
Base = declarative_base()

def get_db():     
    db = SessionLocal()     
    try:         
        yield db     
    finally:
        db.close()
