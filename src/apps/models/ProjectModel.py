from sqlalchemy import func

from src.SharedServices.MainService import MainService
from src.apps.models import OperationCls
from src.config.extension import db


class Project(db.Model):
    __tablename__ = 'project'

    id_project = db.Column(db.Integer, primary_key=True, unique=True)
    id_customer = db.Column(db.Integer, db.ForeignKey('customers.id_customer'), nullable=True)
    project_name = db.Column(db.String(100), nullable=True)
    date_add = db.Column(db.DateTime, default=MainService.getDateTimeNow(), nullable=True)

    # activities = db.relationship('Activity', backref='project', lazy=True)

    def __repr__(self):
        return f"project: {self.id_project}"

    def __init__(self, data):
        self.id_customer = data.get('id_customer', None)
        self.project_name = data.get('project_name', None)

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
            results = Project.query.filter(func.lower(Project.project_name) == func.lower(name)).first()
        except Exception as e:
            print(f"Query exception --> {e}")
            results = None
        finally:
            db.session.remove()
        return results
