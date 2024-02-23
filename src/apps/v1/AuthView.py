from flask import Blueprint, request

from src.SharedServices.Authentication import Auth
from src.SharedServices.MainService import MainService, StatusType
from src.apps.models.UserModel import User

authApi = Blueprint('Auth view version 1', __name__)


@authApi.route('/signup', methods=['POST'])
def signup():
    data = request.json
    errors = MainService.validation(fields=['name', 'surname', 'username', 'github_user', 'mail', 'password'],
                                    data=data)
    if errors:
        response = {
            "status": StatusType.error.value,
            "data": errors,
            "message": ""
        }
        return MainService.response(data=response, status_code=200)
    print(f"data --> {data}")
    user = User.getUserByEmail(data.get('mail', None))
    if user:
        data = {
            "status": StatusType.fail.value,
            "data": None,
            "message": "Email is already exist!"
        }
        return MainService.response(data=data, status_code=200)
    user = User.getUserByUsername(data.get('username', None))
    if user:
        data = {
            "status": StatusType.fail.value,
            "data": None,
            "message": "Username is already exist!"
        }
        return MainService.response(data=data, status_code=200)
    user = User(data)
    user.save()
    id_user = user.id_user
    token = Auth.generate_token(id_user)
    # Send response
    data = {
        "status": StatusType.success.value,
        "data": {"token": token, "id_user": id_user},
        "message": "Signup successfully!"
    }
    return MainService.response(data=data, status_code=200)


@authApi.route('/login', methods=['POST'])
def login():
    data = request.json
    errors = MainService.validation(fields=['mail', 'password'], data=data)
    if errors:
        response = {
            "status": StatusType.error.value,
            "data": errors,
            "message": ""
        }
        return MainService.response(data=response, status_code=200)
    user = User.getUserByEmail(data.get('mail', None))
    if user is None:
        data = {
            "status": StatusType.fail.value,
            "data": None,
            "message": "Email is not exist!"
        }
        return MainService.response(data=data, status_code=200)
    isValid = User.verifyPassword(user.password, data.get('password', ''))
    if isValid:
        id_user = user.id_user
        token = Auth.generate_token(id_user)
        # Send response
        data = {
            "status": StatusType.success.value,
            "data": {"token": token, "id_user": id_user},
            "message": "Login successfully!"
        }
        return MainService.response(data=data, status_code=200)
    else:
        data = {
            "status": StatusType.fail.value,
            "data": None,
            "message": "Login failed!"
        }
        return MainService.response(data=data, status_code=200)
