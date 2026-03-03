import logging

from flask import Flask
from config import Config

from app.extensions import db, migrate, login_manager


def create_app(config_class=Config):
    """
    Factory da aplicação. Cria e configura uma instância do Flask.
    """
    app = Flask(__name__)
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
