from app import db
from sqlalchemy.orm import relationship


class Lembretes(db.Model):
    __tablename__ = "Lembretes"
    
    id = db.Column(db.Integer, primary_key=True)
    clienteId = db.Column(db.Integer, db.ForeignKey("Clientes.id"), nullable=False)
    produtoId = db.Column(db.Integer, db.ForeignKey("Products.id"), nullable=False)
    clienteName = db.Column(db.String(120))
    produtoName = db.Column(db.String(120))
    valor = db.Column(db.Float, nullable=False)
    time = db.Column(db.String(80), nullable=False)
    timer = db.Column(db.Integer)


    cliente = relationship("Clientes", back_populates="lembretes")
    produto = relationship("Products", back_populates="lembretes")

    def __init__(self, *, clienteName, produtoName, valor, time, timer, clienteId=None, produtoId=None):
        self.clienteName = clienteName
        self.produtoName = produtoName
        self.valor = valor
        self.time = time
        self.timer = timer
        self.clienteId = clienteId
        self.produtoId = produtoId



    def __repr__(self):
        return '<Lembretes %r>' % self.clienteName