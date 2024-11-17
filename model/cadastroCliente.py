from app import db
from sqlalchemy.orm import relationship


class Clientes(db.Model):
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