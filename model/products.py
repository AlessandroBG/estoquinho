from app import db


class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    productName = db.Column(db.String(80), nullable=False)
    productPrice = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return '<Products %r>' % self.productName