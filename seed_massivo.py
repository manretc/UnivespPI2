import os
import sys
import random
from datetime import datetime, timedelta
from faker import Faker

sys.path.append(os.getcwd())

from app import create_app, db
from app.models import User, Donation

app = create_app()
faker = Faker('pt_BR')

def seed_massivo(n=1000):
    with app.app_context():
        print("🧹 Limpando banco de dados para o novo setup...")
        db.session.query(Donation).delete()
        db.session.query(User).delete()
        db.session.commit()

        # 1. Criar o seu usuário de acesso (Admin/Teste)
        print("👤 Criando seu usuário de acesso...")
        admin = User(username='leandro', email='leandro@teste.com', user_type='donor')
        admin.set_password('123456')
        db.session.add(admin)

        # 2. Criar os 97 Doadores (subtraindo o admin)
        print("👥 Gerando 96 doadores adicionais...")
        doadores = [admin]
        for _ in range(96):
            u = User(username=faker.user_name(), email=faker.email(), user_type='donor')
            u.set_password('123456')
            db.session.add(u)
            doadores.append(u)

        # 3. Criar as 28 Instituições
        print("🏢 Gerando 28 instituições parceiras...")
        instituicoes = []
        for _ in range(28):
            i = User(username=faker.company(), email=faker.email(), user_type='inst')
            i.set_password('123456')
            db.session.add(i)
            instituicoes.append(i)
        
        db.session.commit()

        print(f"🌱 Distribuindo {n} doações entre os usuários...")
        status_opcoes = ['available', 'claimed', 'collected']
        alimentos = ['Arroz', 'Feijão', 'Macarrão', 'Leite em Pó', 'Óleo', 'Cesta Básica', 'Açúcar', 'Café']
        
        for i in range(n):
            dias_atras = random.randint(1, 365)
            # 2026 é o ano atual no sistema
            data_aleatoria = datetime.utcnow() - timedelta(days=dias_atras)
            
            status_sorteado = random.choice(status_opcoes)
            
            # Se a doação foi reservada ou coletada, atribuímos a uma instituição aleatória
            inst_recolha = random.choice(instituicoes) if status_sorteado != 'available' else None

            nova_doacao = Donation(
                description=f"{random.choice(alimentos)} - Lote {faker.bothify(text='##??')}",
                quantity=f"{random.randint(2, 50)} unidades",
                status=status_sorteado,
                user_id=random.choice(doadores).id,
                claimed_by_id=inst_recolha.id if inst_recolha else None,
                address=faker.address(),
                latitude=-23.5 + random.uniform(-0.2, 0.2), # Pequena variação em SP
                longitude=-46.6 + random.uniform(-0.2, 0.2),
                created_at=data_aleatoria
            )
            db.session.add(nova_doacao)

        db.session.commit()
        print(f"✅ Setup concluído: 97 Doadores, 28 Instituições e {n} Doações!")

if __name__ == '__main__':
    seed_massivo()