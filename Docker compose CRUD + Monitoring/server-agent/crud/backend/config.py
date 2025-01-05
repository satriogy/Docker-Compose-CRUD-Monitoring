import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://myuser:mypassword@postgres:5432/mydatabase'
    UPLOAD_FOLDER = 'uploads/'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
