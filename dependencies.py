from fastapi import Depends, HTTPException
from models import db, Usuario
from sqlalchemy.orm import sessionmaker, Session
from main import oauth2_schema, SECRET_KEY, ALGORITHM
from jose import jwt, JWTError

def pegar_sessao():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        session.close()
    
# verificar token de autenticacao
def verificar_token(token: str = Depends(oauth2_schema), session: Session = Depends(pegar_sessao)):
    try:
        dic_info = jwt.decode(token, SECRET_KEY, ALGORITHM)
        id_usuario = int(dic_info.get("sub"))
    except JWTError:
        raise HTTPException(status_code=401, detail="acesso negado")
    usuario = session.query(Usuario).filter(Usuario.id==id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="acesso invalido")
    return usuario

