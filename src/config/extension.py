from flask_mail import Mail
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


# SQLAlchemy initialize
db = SQLAlchemy()

# Marshmallow initialize
ma = Marshmallow()

mail = Mail()

socketio = SocketIO()


