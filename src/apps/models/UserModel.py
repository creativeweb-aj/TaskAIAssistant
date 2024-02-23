from sqlalchemy import func
from src.SharedServices.MainService import MainService
from src.config.extension import db
import bcrypt


class User(db.Model):
    __tablename__ = 'user'

    id_user = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(100), nullable=True)
    surname = db.Column(db.String(100), unique=True, nullable=True)
    username = db.Column(db.String(100), nullable=True)
    password = db.Column(db.String(100), nullable=True)
    mail = db.Column(db.String(100), nullable=True)
    github_user = db.Column(db.String(100), nullable=True)
    date_add = db.Column(db.DateTime, default=MainService.getDateTimeNow(), nullable=True)

    # activities = db.relationship('Activity', backref='user', lazy=True)

    def __repr__(self):
        return f"user: {self.id_user}"

    def __init__(self, data):
        print(f"User data --> {data}")
        self.name = data.get('name', None)
        self.surname = data.get('surname', None)
        self.username = data.get('username', None)
        self.password = self.hashPassword(data.get('password', ''))
        self.mail = data.get('mail', None)
        self.github_user = data.get('github_user', None)

    @staticmethod
    def verifyPassword(hashed_password, input_password):
        # Convert the input password to bytes
        input_password = input_password.encode('utf-8')

        # Compare the input password hash with the stored hash
        return bcrypt.checkpw(input_password, hashed_password.encode('utf-8'))

    @staticmethod
    def hashPassword(password):
        # Convert the password to bytes
        password = password.encode('utf-8')

        # Generate a salt and hash the password
        hashed = bcrypt.hashpw(password=password, salt=bcrypt.gensalt())

        # Decoding the byte string to a regular string
        hashed = hashed.decode('utf-8')
        return hashed

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
    def getUserById(value):
        try:
            results = User.query.filter(User.id_user == value).first()
        except Exception as e:
            print(f"Query exception --> {e}")
            results = None
        finally:
            db.session.remove()
        return results

    @staticmethod
    def getUserByEmail(value):
        try:
            results = User.query.filter(func.lower(User.mail) == func.lower(value)).first()
        except Exception as e:
            print(f"Query exception --> {e}")
            results = None
        finally:
            db.session.remove()
        return results

    @staticmethod
    def getUserByUsername(value):
        try:
            results = User.query.filter(func.lower(User.username) == func.lower(value)).first()
        except Exception as e:
            print(f"Query exception --> {e}")
            results = None
        finally:
            db.session.remove()
        return results
