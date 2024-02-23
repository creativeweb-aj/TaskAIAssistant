import os

# Secret Key
SECRET_KEY = os.environ.get('SECRET_KEY', '')

# Database configurations
SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI', '')
SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS', True)

# Upload media files folders
UPLOAD_FOLDER = os.path.join(os.path.abspath('media') + '/uploads')

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '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')
