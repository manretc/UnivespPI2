import os
import logging

from flask import Flask
from config import Config
from dotenv import load_dotenv

from app.extensions import db, migrate, login_manager

load_dotenv()

def create_app(config_class=Config):
    """
    Factory da aplicação. Cria e configura uma instância do Flask.
    """
    app = Flask(__name__)

    app.config["SECRET_KEY"] = "sua_chave_secreta"
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.config.from_object(config_class)

    # Inicializa extensões
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    logging.basicConfig(level=logging.INFO)

    # Registro de blueprints
    from app.routes import bp as main_bp
    app.register_blueprint(main_bp)

    # Importa modelos para evitar import circular
    with app.app_context():
        from app import models

    return app
