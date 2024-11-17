from app import db
from sqlalchemy.orm import relationship


class Products(db.Model):
    __tablename__ = "Products"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)
    qtd = db.Column(db.Integer, nullable=False)
    

    lembretes = relationship("Lembretes", back_populates="produto")


    def __repr__(self):
        return '<Products %r>' % self.Name