# tests/test_basic.py
# Arquivo inicial para testes.
# Usando pytest, podemos escrever testes simples para garantir que a aplicação
# está funcionando como esperado.

import unittest
from app import create_app, db
from app.models import User
from config import Config


class TestConfig(Config):
    """Configuração de teste para usar um banco de dados em memória."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'  # Usa SQLite em memória para os testes


class BasicTests(unittest.TestCase):
    def setUp(self):
        """
        Este método é executado antes de cada teste.
        Cria uma instância da aplicação com a configuração de teste e
        cria todas as tabelas do banco de dados.
        """
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        """
        Este método é executado após cada teste.
        Remove a sessão do banco de dados e apaga todas as tabelas.
        """
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exists(self):
        """Teste para verificar se a aplicação é criada com sucesso."""
        self.assertFalse(self.app is None)

    def test_app_is_testing(self):
        """Teste para verificar se a aplicação está em modo de teste."""
        self.assertTrue(self.app.config['TESTING'])

    def test_index_page(self):
        """Teste para verificar se a página inicial carrega corretamente."""
        tester = self.app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        # CORREÇÃO: O teste agora procura pelo texto exato com a acentuação correta.
        # O 'b' antes da string indica que estamos a comparar bytes, que é como o
        # Flask envia os dados da resposta.
        self.assertTrue(b'Rede de Doa\xc3\xa7\xc3\xb5es' in response.data)


if __name__ == "__main__":
    unittest.main()
