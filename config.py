# config.py
# Arquivo de configuração da aplicação.
# Centraliza todas as configurações, facilitando a gestão para diferentes ambientes
# (desenvolvimento, produção, testes).

import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
# Isso permite manter informações sensíveis (como senhas e chaves de API)
# fora do código-fonte.
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config:
    """
    Configurações base que são compartilhadas por todos os ambientes.
    """
    # Chave secreta para proteger sessões e cookies.
    # É crucial para a segurança contra ataques CSRF.
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'uma-chave-secreta-muito-dificil-de-adivinhar'

    # Configuração do banco de dados SQLAlchemy.
    # A URI é lida da variável de ambiente DATABASE_URL.
    # Se não for encontrada, usa um banco de dados SQLite local como fallback.
    _database_url = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    # Render fornece postgres:// mas SQLAlchemy 2.0+ exige postgresql://
    if _database_url.startswith('postgres://'):
        _database_url = _database_url.replace('postgres://', 'postgresql://', 1)
    SQLALCHEMY_DATABASE_URI = _database_url

    # Desativa o rastreamento de modificações do SQLAlchemy para economizar recursos,
    # pois não estamos usando o sistema de eventos do Flask-SQLAlchemy.
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Chave da API do Google Maps, lida das variáveis de ambiente.
    GOOGLE_MAPS_API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY')
