# tests/test_functional.py
# Versão FINAL com correção para codificação de caracteres (UTF-8).

import unittest
from unittest.mock import patch
from flask import url_for

from app import create_app, db
from app.models import User, Donation
from config import Config


class TestConfig(Config):
    """Configuração de teste para usar um banco de dados em memória."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    WTF_CSRF_ENABLED = False
    SERVER_NAME = 'localhost'


class FunctionalTests(unittest.TestCase):
    def setUp(self):
        """Este método é executado antes de cada teste."""
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        """Este método é executado após cada teste."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    @patch('app.routes.geocode_address', return_value=(-23.5, -46.6))
    def test_user_registration_and_login(self, mock_geocode):
        """Testa o registo de um novo utilizador e o seu posterior login."""
        response = self.client.post(
            url_for('main.register'),
            data={
                'username': 'testuser',
                'email': 'test@example.com',
                'password': 'password123',
                'password2': 'password123',
                'user_type': 'donor',
                'address': 'Rua Teste, 123, Cidade Teste'
            },
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        # CORREÇÃO: Usa a string correta e codifica para bytes (utf-8)
        self.assertIn("Parabéns, você foi registrado com sucesso!".encode('utf-8'), response.data)

        response = self.client.post(
            url_for('main.login'),
            data={'username': 'testuser', 'password': 'password123'},
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Seu Painel, testuser!', response.data)

    @patch('app.routes.geocode_address', return_value=(-23.5, -46.6))
    def test_edit_profile(self, mock_geocode):
        """Testa a funcionalidade de edição de perfil de um utilizador."""
        user = User(username='edituser', email='edit@example.com', user_type='donor', address='Endereço Antigo')
        user.set_password('password')
        db.session.add(user)
        db.session.commit()
        self.client.post(url_for('main.login'), data={'username': 'edituser', 'password': 'password'},
                         follow_redirects=True)

        response = self.client.post(
            url_for('main.editar_perfil'),
            data={
                'username': 'edituser_novo',
                'email': 'edit_novo@example.com',
                'address': 'Endereço Novo, 456'
            },
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Seu perfil foi atualizado com sucesso!', response.data)

        updated_user = User.query.filter_by(username='edituser_novo').first()
        self.assertIsNotNone(updated_user)
        self.assertEqual(updated_user.address, 'Endereço Novo, 456')

    @patch('app.routes.geocode_address', return_value=(-23.5, -46.6))
    def test_full_donation_cycle(self, mock_geocode):
        """Testa o ciclo de vida completo de uma doação."""
        donor = User(username='doador', email='doador@example.com', user_type='donor', address='Rua do Doador, 1',
                     latitude=-23.5, longitude=-46.6)
        donor.set_password('pass')
        db.session.add(donor)
        db.session.commit()
        self.client.post(url_for('main.login'), data={'username': 'doador', 'password': 'pass'}, follow_redirects=True)

        response = self.client.post(
            url_for('main.create_donation'),
            data={'description': 'Cesta basica', 'quantity': '10', 'address': ''},
            follow_redirects=True
        )
        # CORREÇÃO: Usa a string correta e codifica para bytes (utf-8)
        self.assertIn("Sua doação foi registrada com sucesso!".encode('utf-8'), response.data)
        donation = Donation.query.first()
        self.assertIsNotNone(donation)

        self.client.get(url_for('main.logout'), follow_redirects=True)

        charity = User(username='instituicao', email='charity@example.com', user_type='charity',
                       address='Rua da Instituicao, 2', latitude=-23.6, longitude=-46.7)
        charity.set_password('pass')
        db.session.add(charity)
        db.session.commit()
        self.client.post(url_for('main.login'), data={'username': 'instituicao', 'password': 'pass'},
                         follow_redirects=True)

        response = self.client.post(url_for('main.claim_donation', donation_id=donation.id), follow_redirects=True)
        # CORREÇÃO: Usa a string correta e codifica para bytes (utf-8)
        self.assertIn("Doação reservada com sucesso!".encode('utf-8'), response.data)

        self.client.get(url_for('main.logout'), follow_redirects=True)

        self.client.post(url_for('main.login'), data={'username': 'doador', 'password': 'pass'}, follow_redirects=True)

        response = self.client.post(url_for('main.confirm_collection', donation_id=donation.id), follow_redirects=True)
        # CORREÇÃO: Usa a string correta e codifica para bytes (utf-8)
        self.assertIn("Recolhimento da doação confirmado com sucesso!".encode('utf-8'), response.data)


    def test_login_with_invalid_credentials(self):
        """Testa login com credenciais invalidas mostra mensagem de erro."""
        response = self.client.post(
            url_for('main.login'),
            data={'username': 'naoexiste', 'password': 'senhaerrada'},
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("Usuário ou senha inválidos".encode('utf-8'), response.data)

    @patch('app.routes.geocode_address', return_value=(None, None))
    def test_register_with_geocode_failure(self, mock_geocode):
        """Testa que usuario nao e criado quando geocode falha."""
        response = self.client.post(
            url_for('main.register'),
            data={
                'username': 'testgeo',
                'email': 'geo@example.com',
                'password': 'password123',
                'password2': 'password123',
                'user_type': 'donor',
                'address': 'Endereco Invalido'
            },
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("Não foi possível encontrar as coordenadas".encode('utf-8'), response.data)
        user = User.query.filter_by(username='testgeo').first()
        self.assertIsNone(user)

    @patch('app.routes.geocode_address', return_value=(-23.5, -46.6))
    def test_donor_cannot_claim_donation(self, mock_geocode):
        """Testa que doador nao pode reservar doacoes (apenas instituicoes)."""
        donor = User(username='doador2', email='doador2@example.com', user_type='donor',
                     address='Rua do Doador, 1', latitude=-23.5, longitude=-46.6)
        donor.set_password('pass')
        db.session.add(donor)
        db.session.commit()

        donation = Donation(description='Teste', quantity='5', donor=donor,
                            address='Rua Teste', latitude=-23.5, longitude=-46.6)
        db.session.add(donation)
        db.session.commit()

        self.client.post(url_for('main.login'),
                         data={'username': 'doador2', 'password': 'pass'},
                         follow_redirects=True)

        response = self.client.post(
            url_for('main.claim_donation', donation_id=donation.id),
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("Apenas instituições podem reservar doações.".encode('utf-8'), response.data)
        # Doacao continua disponivel
        donation = Donation.query.get(donation.id)
        self.assertEqual(donation.status, 'available')


if __name__ == '__main__':
    unittest.main()