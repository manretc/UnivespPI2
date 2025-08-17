# run.py
# Ponto de entrada principal da aplicação.
# Este script importa a instância da aplicação criada na factory (create_app)
# e a executa. É o arquivo que você rodará para iniciar o servidor.

from app import create_app, db
from app.models import User, Donation

# Cria a instância da aplicação usando a factory
app = create_app()

# O contexto da aplicação (app_context) torna a instância da aplicação
# acessível para extensões como o Flask-SQLAlchemy.
# Isso é útil para testes e para o shell do Flask.
@app.shell_context_processor
def make_shell_context():
    """
    Configura o contexto do shell do Flask para facilitar a depuração.
    Permite usar 'flask shell' e ter acesso direto a 'db', 'User' e 'Donation'.
    """
    return {'db': db, 'User': User, 'Donation': Donation}

if __name__ == '__main__':
    # Inicia o servidor de desenvolvimento do Flask.
    # O modo de depuração (debug=True) ativa o recarregamento automático
    # e exibe informações detalhadas de erros no navegador.
    # Não use o modo de depuração em um ambiente de produção.
    app.run(debug=True)
