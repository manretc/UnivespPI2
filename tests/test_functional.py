# tests/test_functional.py
import unittest
from unittest.mock import patch
from flask import url_for
from app import create_app, db
from app.models import User, Donation
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    WTF_CSRF_ENABLED = False
    SERVER_NAME = 'localhost'


class FunctionalTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    @patch('app.routes.geocode_address', return_value=(-23.5, -46.6))
    def test_user_registration_navbar_and_login(self, mock_geocode):
        """Testa registo e login (verificando se o botão Início desaparece)."""
        # Registro usando a chave interna 'donor' (que o formulário espera)
        self.client.post(
            url_for('main.register'),
            data={
                'username': 'testuser',
                'email': 'test@example.com',
                'password': 'password123',
                'password2': 'password123',
                'user_type': 'donor',
                'address': 'Rua Teste, 123'
            },
            follow_redirects=True
        )

        # Login
        response = self.client.post(
            url_for('main.login'),
            data={'username': 'testuser', 'password': 'password123'},
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)
        # Verifica se o Painel aparece (usuário logado com sucesso)
        self.assertIn(b'Painel', response.data)
        # Verifica se o botão 'Início' sumiu conforme a lógica da base.html
        self.assertNotIn("Início".encode('utf-8'), response.data)

    @patch('app.routes.geocode_address', return_value=(-23.5, -46.6))
    def test_full_donation_cycle(self, mock_geocode):
        """Testa o ciclo completo: criar, reservar e confirmar coleta."""
        donor = User(username='doador', email='doador@example.com', user_type='donor', address='Rua A')
        donor.set_password('pass')
        charity = User(username='instituicao', email='charity@example.com', user_type='charity', address='Rua B')
        charity.set_password('pass')
        db.session.add_all([donor, charity])
        db.session.commit()

        # 1. Login do Doador
        self.client.post(url_for('main.login'), data={'username': 'doador', 'password': 'pass'}, follow_redirects=True)

        # 2. Criar Doação
        self.client.post(url_for('main.create_donation'),
                         data={'description': 'Cesta Básica', 'quantity': '5', 'address': 'Rua A'},
                         follow_redirects=True)

        donation = Donation.query.first()
        self.assertIsNotNone(donation, "A doação deveria ter sido criada.")
        self.client.get(url_for('main.logout'), follow_redirects=True)

        # 3. Login da Instituição e Reserva
        self.client.post(url_for('main.login'), data={'username': 'instituicao', 'password': 'pass'},
                         follow_redirects=True)
        response = self.client.post(url_for('main.claim_donation', donation_id=donation.id), follow_redirects=True)
        self.assertIn("Doação reservada com sucesso!".encode('utf-8'), response.data)
        self.client.get(url_for('main.logout'), follow_redirects=True)

        # 4. Login do Doador e Confirmação
        self.client.post(url_for('main.login'), data={'username': 'doador', 'password': 'pass'}, follow_redirects=True)
        response = self.client.post(url_for('main.confirm_collection', donation_id=donation.id), follow_redirects=True)
        self.assertIn("Recolhimento da doação confirmado com sucesso!".encode('utf-8'), response.data)

    def test_impacto_page_renders_correctly(self):
        """Verifica se a página de impacto exibe doadores com doações CONCLUÍDAS."""
        donor = User(username='doador_imp', email='imp@test.com', user_type='donor', address='Rua A')
        donor.set_password('pass')
        db.session.add(donor)
        db.session.commit()

        # Cria uma doação já com status 'collected' para aparecer no ranking
        donation = Donation(
            description='Leite',
            quantity='10',
            status='collected',
            user_id=donor.id,
            address='Rua A',
            latitude=0,
            longitude=0
        )
        db.session.add(donation)
        db.session.commit()

        response = self.client.get(url_for('main.impacto'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Impacto Social', response.data)
        # Agora o nome deve aparecer pois existe uma doação concluída
        self.assertIn(b'doador_imp', response.data)


if __name__ == '__main__':
    unittest.main()