from app import db


class Clientes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    cpf = db.Column(db.String(80), nullable=False)
    endereco = db.Column(db.String(120), nullable=False)
    telefone = db.Column(db.String(80), nullable=False)


    def __repr__(self):
        return '<Clientes %r>' % self.name