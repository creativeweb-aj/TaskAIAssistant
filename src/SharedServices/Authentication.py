import jwt
import os
import datetime
from flask import request
from functools import wraps
from src.SharedServices.MainService import MainService, StatusType
from src.config.configurations import SECRET_KEY


class Auth:
    """
    Auth Class
    """

    @staticmethod
    def generate_token(user_id):
        """
        Generate Token Method
        """
        try:
            currentDateTime = datetime.datetime.utcnow()
            expireDateTime = currentDateTime + datetime.timedelta(days=90)
            payload = {
                'exp': expireDateTime,
                'iat': currentDateTime,
                'user_id': user_id
            }
            token = jwt.encode(
                payload=payload,
                key=os.getenv('SECRET_KEY'),
                algorithm='HS256'
            )
            try:
                if "b'" in str(token):
                    token = token.decode('utf-8')
            except Exception as e:
                print(f"Token generating error ==> {e}")
                pass
            return token

        except Exception as e:
            print(f"Token error ==> {e}")
            response = {
                "status": StatusType.fail.value,
                "data": None,
                "message": f"Error in generating user token: {str(e)}"
            }
            return MainService.response(data=response, status_code=403)

    @staticmethod
    def auth_required(func):
        """
        Auth decorator
        """

        @wraps(func)
        def decorated_auth(*args, **kwargs):
            token = None
            defaultLang = "en"
            if 'Accept-Language' in request.headers:
                langCode = request.headers.get('Accept-Language', defaultLang)
                if langCode is None or langCode == "":
                    langCode = defaultLang
            else:
                langCode = defaultLang
            # jwt is passed in the request header
            if 'Authorization' in request.headers:
                token = request.headers['Authorization']
                token = token.split(' ')[1]
            # return 401 if token is not passed
            if not token:
                response = {
                    "status": StatusType.fail.value,
                    "data": None,
                    "message": "Token is missing!"
                }
                return MainService.response(data=response, status_code=401)
            try:
                # decoding the payload to fetch the stored details
                data = jwt.decode(
                    jwt=token,
                    key=SECRET_KEY,
                    algorithms=["HS256"],
                )
                idUser = data.get('customer_id', None)
            except jwt.ExpiredSignatureError:
                response = {
                    "status": StatusType.fail.value,
                    "data": None,
                    "message": "Token expired, please login again!"
                }
                return MainService.response(data=response, status_code=401)
            except jwt.InvalidTokenError:
                response = {
                    "status": StatusType.fail.value,
                    "data": None,
                    "message": "Invalid token, please try again with a new token!"
                }
                return MainService.response(data=response, status_code=401)
            return func(idUser, langCode, *args, **kwargs)

        return decorated_auth

    @staticmethod
    def decodeToken(token):
        res = {
            "id_user": None,
            "token": True
        }
        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(
                jwt=token,
                key=os.getenv('SECRET_KEY'),
                algorithms=["HS256"],
            )
            res['id_user'] = data.get('user_id', '')
        except jwt.ExpiredSignatureError:
            res['token'] = False
            print(f"ExpiredSignatureError --> {jwt.ExpiredSignatureError}")
        except jwt.InvalidTokenError:
            res['token'] = False
            print(f"InvalidTokenError --> {jwt.InvalidTokenError}")
        return res
