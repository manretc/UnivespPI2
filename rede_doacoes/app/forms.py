# app/forms.py
# Define os formulários web usando a biblioteca Flask-WTF.
# Isso simplifica a criação de formulários, validação de dados e proteção contra CSRF.

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User

class LoginForm(FlaskForm):
    """Formulário de login."""
    username = StringField('Usuário', validators=[DataRequired(message="Campo obrigatório.")])
    password = PasswordField('Senha', validators=[DataRequired(message="Campo obrigatório.")])
    remember_me = BooleanField('Lembrar-me')
    submit = SubmitField('Entrar')

class RegistrationForm(FlaskForm):
    """Formulário de registro."""
    username = StringField('Nome de Usuário', validators=[DataRequired(message="Campo obrigatório.")])
    email = StringField('Email', validators=[DataRequired(message="Campo obrigatório."), Email(message="Email inválido.")])
    password = PasswordField('Senha', validators=[DataRequired(message="Campo obrigatório.")])
    password2 = PasswordField(
        'Repita a Senha', validators=[DataRequired(message="Campo obrigatório."), EqualTo('password', message="As senhas devem ser iguais.")])
    user_type = SelectField('Tipo de Conta', choices=[('donor', 'Doador'), ('charity', 'Instituição')], validators=[DataRequired()])
    address = StringField('Endereço Completo (Rua, Número, Cidade, Estado)', validators=[DataRequired(message="Campo obrigatório.")])
    submit = SubmitField('Registrar')

    def validate_username(self, username):
        """Valida se o nome de usuário já existe no banco de dados."""
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Este nome de usuário já está em uso. Por favor, escolha outro.')

    def validate_email(self, email):
        """Valida se o e-mail já existe no banco de dados."""
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Este e-mail já está registrado. Por favor, use outro.')

class DonationForm(FlaskForm):
    """Formulário para registrar uma nova doação."""
    description = TextAreaField('Descrição dos Alimentos', validators=[DataRequired(message="Campo obrigatório.")])
    quantity = StringField('Quantidade (ex: 3 caixas, 10 kg)', validators=[DataRequired(message="Campo obrigatório.")])
    address = StringField('Endereço de Coleta (deixe em branco para usar o endereço do seu cadastro)')
    submit = SubmitField('Registrar Doação')
