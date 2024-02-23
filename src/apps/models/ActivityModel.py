from sqlalchemy import func

from src.apps.models import OperationCls
from src.config.extension import db


class Activity(db.Model):
    __tablename__ = 'activities'

    id_activity = db.Column(db.Integer, primary_key=True, unique=True)
    id_user = db.Column(db.Integer, nullable=True)
    id_project = db.Column(db.Integer, nullable=True)
    activity_name = db.Column(db.String(100), nullable=True)
    description = db.Column(db.Text, nullable=True)
    hours = db.Column(db.Integer, nullable=True)
    date = db.Column(db.DateTime, nullable=True)
    time = db.Column(db.DateTime, server_default=func.now(), nullable=True)

    def __repr__(self):
        return f"activities: {self.id_activity}"

    def __init__(self, data):
        self.id_user = data.get('id_user', None)
        self.id_project = data.get('id_project', None)
        self.activity_name = data.get('activity_name', None)
        self.description = data.get('description', None)
        self.hours = data.get('hours', None)
        self.date = data.get('date', None)

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