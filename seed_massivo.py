import os
import sys
import random
from datetime import datetime, timedelta
from faker import Faker

# Garante que o Python encontre a pasta 'app'
sys.path.append(os.getcwd())

from app import create_app, db
from app.models import User, Donation # <-- Usando os nomes corretos agora

app = create_app()
faker = Faker('pt_BR')

def seed_massivo(n=1000):
    with app.app_context():
        print("🧹 Limpando doações antigas para resetar o gráfico...")
        db.session.query(Donation).delete()
        db.session.commit()

        # Precisamos de pelo menos um usuário para ser o 'dono' das doações
        user = User.query.first()
        if not user:
            print("❌ Erro: Nenhum usuário encontrado no banco. Crie um usuário primeiro.")
            return

        print(f"🌱 Gerando {n} doações espalhadas pelo ano de 2025/2026...")
        
        for i in range(n):
            # Sorteia uma data nos últimos 365 dias para espalhar no gráfico
            dias_atras = random.randint(1, 365)
            data_aleatoria = datetime.utcnow() - timedelta(days=dias_atras)
            
            nova_doacao = Donation(
                description=f"{random.choice(['Cesta Básica', 'Arroz', 'Feijão', 'Leite', 'Frutas'])} - {faker.word()}",
                quantity=f"{random.randint(1, 50)} kg",
                status=random.choice(['available', 'claimed', 'collected']),
                user_id=user.id,
                address=faker.address(),
                latitude=user.latitude or -23.5505, # Usa a do user ou SP como padrão
                longitude=user.longitude or -46.6333,
                created_at=data_aleatoria # O campo que o seu gráfico usa!
            )
            db.session.add(nova_doacao)
            
            if (i + 1) % 250 == 0:
                print(f"--- {i + 1} doações criadas...")
        
        db.session.commit()
        print(f"🚀 Sucesso! {n} doações criadas com datas variadas.")

if __name__ == '__main__':
    seed_massivo()