import os


class Config:
    SECRET_KEY = "sua_chave_secreta"
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'store.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
