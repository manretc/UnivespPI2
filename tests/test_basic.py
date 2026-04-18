# tests/test_basic.py
import unittest
from app import create_app, db
from app.models import User
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class BasicTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exists(self):
        self.assertFalse(self.app is None)

    def test_index_page_content(self):
        """Verifica se a página inicial carrega os novos textos e seções."""
        tester = self.app.test_client(self)
        response = tester.get('/')
        self.assertEqual(response.status_code, 200)

        # Verifica o título principal
        self.assertIn("Rede de Doações".encode('utf-8'), response.data)

        # Verifica os novos botões solicitados
        self.assertIn("Faça Parte".encode('utf-8'), response.data)
        self.assertIn("Já tenho uma conta".encode('utf-8'), response.data)

        # Verifica se as novas seções de informação estão presentes
        self.assertIn("Quem Somos".encode('utf-8'), response.data)
        self.assertIn("Guia Detalhado de Utilização".encode('utf-8'), response.data)

    def test_health_endpoint(self):
        tester = self.app.test_client()
        response = tester.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"status": "ok"})

    def test_dashboard_requires_login(self):
        tester = self.app.test_client()
        response = tester.get('/dashboard')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.headers['Location'])