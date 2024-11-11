from app import db


class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)
    qtd = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Products %r>' % self.productName