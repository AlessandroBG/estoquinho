from app import db
from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Clientes(db.Model, Base):
    __tablename__ = "Clientes"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    cpf = db.Column(db.String(80), nullable=False)
    endereco = db.Column(db.String(120), nullable=False)
    telefone = db.Column(db.String(80), nullable=False)
    children = relationship("Lembretes")


    lembretes = relationship("Lembretes", back_populates="cliente")


    def __repr__(self):
        return '<Clientes %r>' % self.name