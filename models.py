
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from database import Base
from sqlalchemy.orm import relationship


class Todos(Base):
    __tablename__ = 'Todos'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("Users.id"))
    
    owner = relationship("Users", back_populates="todos")


class Users(Base):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, unique=True)
    email = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    # La siguiente linea se escribe para relacionar a owner siendo una foreign key con el id de usuarios
    todos = relationship("Todos", back_populates="owner")