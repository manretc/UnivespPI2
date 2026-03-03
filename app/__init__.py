# app/__init__.py
# Este arquivo inicializa o pacote 'app' e contém a factory da aplicação.
# A factory 'create_app' é um padrão que permite criar múltiplas instâncias
# da aplicação com diferentes configurações, o que é ótimo para testes.
import os
import logging

from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv

# Inicialização das extensões do Flask.
# Elas são criadas aqui, mas inicializadas dentro da factory
# para vincular a uma instância específica da aplicação.

load_dotenv()

login_manager = LoginManager()
# Define a view (rota) para a qual usuários não autenticados serão redirecionados.
login_manager.login_view = 'main.login'
login_manager.login_message = 'Por favor, faça login para acessar esta página.'

def create_app(config_class=Config):
    """
    Factory da aplicação. Cria e configura uma instância do Flask.
    """
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "sua_chave_secreta"
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Carrega as configurações a partir do objeto de configuração.
    app.config.from_object(config_class)

    # Inicializa as extensões com a instância da aplicação.
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    logging.basicConfig(level=logging.INFO)

    # Importa e registra o Blueprint.
    # Blueprints ajudam a organizar a aplicação em componentes modulares.
    # Todas as rotas definidas em 'app.routes' serão registradas sob este blueprint.
    from app.routes import bp as main_bp
    app.register_blueprint(main_bp)

    return app

# Importa os modelos no final para evitar problemas de importação circular.
# O SQLAlchemy precisa conhecer os modelos para criar as tabelas.
from app import models
