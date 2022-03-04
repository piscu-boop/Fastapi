from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
import models
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from database import session_local, engine
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import jwt


SECRET_KEY = "qaz1wsx3edc4rfv6tgb"
ALGORITHM = "HS256"

class Create_User(BaseModel):
    user_name: str
    email: Optional[str]
    firstname: str
    lastname: str
    password: str

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# La siguiente linea creara la base de datos y la tabla con todo lo necesario en caso
# de por alguna razon se ejecute auth.py antes que main.py

models.Base.metadata.create_all(bind=engine)



app = FastAPI()

def get_db():
    try:
        db = session_local()
        yield db
    finally:
        db.close()

def get_password_hash(password):
    return bcrypt_context.hash(password)

def verify_password(plain_password, hashed_password):
    return bcrypt_context.verify(plain_password, hashed_password)
    # El .verify sirve para que el bcrypt context verifique si 
    # la plain password y la hashed password son las mismas

def authenticate_user(user_name: str, password: str, db):
    # En la siguiente instruccion buscamos a ver si existe algun 
    # registro que coincida con el usuario a buscar
    user = db.query(models.Users).filter(models.Users.user_name == user_name).first()

    # Le decimos que si no existe ningun usuario, devuelva falso.
    if not user:
        return False
    # En la siguiente instruccion le decimos que si no esta verificada la 
    # contraseña, que devuelva Falso para indicar que el usuario no es autentificado
    if not verify_password(password, user.hashed_password):
        return False
    return user
    


@app.post("/create/user")
async def create_new_user(create_user: Create_User, db: Session = Depends(get_db)):
    create_user_models = models.Users()
    create_user_models.email = create_user.email
    create_user_models.user_name = create_user.user_name
    create_user_models.first_name = create_user.firstname
    create_user_models.last_name = create_user.lastname
    hash_password = get_password_hash(create_user.password)
    create_user_models.hashed_password = hash_password
    create_user_models.is_active = True

    db.add(create_user_models)
    db.commit()

@app.post("/token")
async def login_for_acces_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session= Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return "User Validated"
    # OAuth2PasswordRequestFormtiene atributos de uso común como 'nombre de usuario', 'contraseña' y 'alcance'.
    # Después de verificar en la base de datos que el usuario existe, se crea un token de acceso para el usuario. 
    # El token de acceso consta de datos que describen al usuario, sus límites de tiempo de acceso y los permisos 
    # de alcance que se le asignan y que se codifica en un objeto compacto de tipo cadena, que es el token.