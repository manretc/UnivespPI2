# app/models.py
# Define a estrutura do banco de dados usando classes de modelo do SQLAlchemy.
# Cada classe representa uma tabela no banco de dados.

from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin, db.Model):
    """
    Modelo para os usuários (doadores e instituições).
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    user_type = db.Column(db.String(10), nullable=False)
    address = db.Column(db.String(200))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    donations = db.relationship('Donation', backref='donor', lazy='dynamic', foreign_keys='Donation.user_id')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        print(f"[check_password] Banco em uso: {engine_url.host} (URL completa: {engine_url})")
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'


class Donation(db.Model):
    """
    Modelo para os alimentos doados.
    """
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255), nullable=False)
    quantity = db.Column(db.String(50), nullable=False)
    # Status: 'available', 'claimed', 'collected'
    status = db.Column(db.String(20), default='available', index=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    address = db.Column(db.String(200), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    # NOVO: Campo para guardar o ID da instituição que irá recolher a doação.
    claimed_by_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    # NOVO: Relacionamento para aceder facilmente ao objeto User da instituição.
    claimed_by = db.relationship('User', foreign_keys=[claimed_by_id])

    def __repr__(self):
        return f'<Donation {self.description}>'


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
