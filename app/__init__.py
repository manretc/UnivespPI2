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

    # Logging com formato estruturado
    logging.basicConfig(
        level=logging.DEBUG if app.debug else logging.INFO,
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )

    # Validacao de variaveis de ambiente no startup
    logger = logging.getLogger(__name__)
    if not app.config.get('GOOGLE_MAPS_API_KEY'):
        logger.warning("GOOGLE_MAPS_API_KEY nao configurada — geocoding desabilitado")
    if app.config.get('SECRET_KEY') == 'uma-chave-secreta-muito-dificil-de-adivinhar' and not app.config.get('TESTING'):
        logger.warning("SECRET_KEY usando valor padrao — defina SECRET_KEY em producao")

    # Security headers
    @app.after_request
    def set_security_headers(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        return response

    # Registro de blueprints
    from app.routes import bp as main_bp
    app.register_blueprint(main_bp)

    # Importa modelos para evitar import circular
    with app.app_context():
        from app import models

    return app
