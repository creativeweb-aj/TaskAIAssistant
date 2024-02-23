from flask import Blueprint
from src.apps.v1.AuthView import authApi
from src.apps.v1.GptView import chatGptApi

apiV1 = Blueprint('API version 1 BluePrints', __name__, url_prefix="v1/")

# Register version 1 API blueprints
apiV1.register_blueprint(authApi)
apiV1.register_blueprint(chatGptApi)
