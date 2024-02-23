import datetime
import enum
import json
import os
import re
from flask import Response, request
from marshmallow import fields, ValidationError
from src.config.configurations import UPLOAD_FOLDER
from werkzeug.utils import secure_filename


class StatusType(enum.Enum):
    success = "SUCCESS"
    fail = "FAIL"
    error = "ERROR"


class Date(enum.Enum):
    format = "%d/%m/%Y"


class FileByte(fields.Field):
    """Field that serializes to a string of numbers and deserializes
    to a list of numbers.
    """

    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return ""
        return "".join(str(d) for d in value)

    def _deserialize(self, value, attr, data, **kwargs):
        try:
            return [int(c) for c in value]
        except ValueError as error:
            raise ValidationError("File bytes must contain only digits.") from error


class DateTimeField(fields.Field):
    """Field that serializes to a string of numbers and deserializes
    to a list of numbers.
    """

    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return ""
        value = float(value)
        date = datetime.datetime.fromtimestamp(int(value))
        date = date.strftime(Date.format.value)
        return date

    def _deserialize(self, value, attr, data, **kwargs):
        try:
            return [int(c) for c in value]
        except ValueError as error:
            raise ValidationError("Datetime field must contain only digits.") from error


def errorResponse(statusCode, message):
    response = json.dumps({
        'status': 'error',
        'message': message
    })
    return Response(mimetype="application/json", response=response, status=statusCode)


class CustomError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class MainService:
    def __init__(self):
        pass

    @staticmethod
    def getDateTimeNow():
        return datetime.datetime.now()

    @staticmethod
    def getCurrentTimeStamp():
        return datetime.datetime.timestamp(datetime.datetime.now())

    # Create response data
    @classmethod
    def responseModel(cls, values):
        if values.get('status') == StatusType.error.value:
            msg = cls.__setErrorMessages(values.get('data', ''))
            response = {
                "status": values.get('status', ''),
                "data": dict(),
                "message": msg,
                "errors": values.get('data', '')
            }
        else:
            try:
                data = json.loads(values.get('data', ''))
            except Exception as e:
                if type(values.get('data', '')) == dict:
                    data = values.get('data', '')
                else:
                    data = dict()
            response = {
                "status": values.get('status', ''),
                "data": data,
                "message": values.get('message', '')
            }
        response = json.dumps(response)
        return response

    # Response method
    @classmethod
    def response(cls, data, status_code):
        """
        Custom Response Function
        """
        response = cls.responseModel(data)
        return Response(
            mimetype="application/json",
            response=response,
            status=status_code
        )

    # Error message create
    @staticmethod
    def __setErrorMessages(data):
        message = ""
        for k, v in data.items():
            if message:
                message = str(message) + str(', ') + str(v)
            else:
                message = str(v)
        return message

    @staticmethod
    def validation(fields: list, data: dict) -> dict:
        errors = {}
        for field in fields:
            name = field.replace('_', ' ')
            if data.get(field) is None or data.get(field) == "":
                errors[field] = f"The {name} field is required."
            else:
                if field == "email":
                    EMAIL_REGEX = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
                    if data.get(field) and not re.match(EMAIL_REGEX, data.get(field)):
                        errors[field] = f"The {name} field is not valid."
                if field == "product":
                    product = data.get(field)
                    for k, v in product.items():
                        if v is None or v == "":
                            n = k.replace('_', ' ')
                            errors[k] = f"The {n} field is required."
        return errors

    # @staticmethod
    # def message(lang):
    #     # Check language code and return message class as refresh according to language
    #     if lang == "en":
    #         return EnglishMessage
    #     elif lang == "it":
    #         return ItalianMessage
    #     else:
    #         return EnglishMessage

    @staticmethod
    def allowed_file(filename):
        ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    @classmethod
    def uploadFile(cls, file):
        if file and cls.allowed_file(file.filename):
            timestamp = cls.getCurrentTimeStamp()
            timestamp = str(timestamp).split('.')[0]
            filename = secure_filename(str(timestamp) + '-' + file.filename)
            filePath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filePath)
            filePath = filePath.split('/media')[-1]
            BaseUrl = request.host_url
            filePath = BaseUrl + 'media' + filePath
            return filePath
        else:
            return None
