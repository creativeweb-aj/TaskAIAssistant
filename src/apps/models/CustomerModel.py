from sqlalchemy import func

from src.SharedServices.MainService import MainService
from src.apps.models import OperationCls
from src.config.extension import db


class Customer(db.Model):
    __tablename__ = 'customers'

    id_customer = db.Column(db.Integer, primary_key=True, unique=True)
    company_name = db.Column(db.String(100), nullable=True)
    date_add = db.Column(db.DateTime, default=MainService.getDateTimeNow(), nullable=True)

    def __repr__(self):
        return f"customers: {self.id_customer}"

    def __init__(self, data):
        self.company_name = data.get('company_name', None)

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        self.save()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def getByName(name):
        try:
            results = Customer.query.filter(func.lower(Customer.company_name) == func.lower(name)).first()
        except Exception as e:
            print(f"Query exception --> {e}")
            results = None
        finally:
            db.session.remove()
        return results
