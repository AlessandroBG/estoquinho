from app import db


class Lembretes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente= db.Column(db.String(80), nullable=False)
    value = db.Column(db.Float, nullable=False)
    time = db.Column(db.String(80), nullable=False)
    timer = db.Column(db.Integer)


    def __repr__(self):
        return '<Products %r>' % self.productName