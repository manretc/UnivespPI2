import random
import math
from datetime import datetime, timedelta

# Importação compatível com a sua estrutura (Local e Render)
try:
    from wsgi import app
except ImportError:
    from app import app

from app import db
from app.models import User, Donation
from werkzeug.security import generate_password_hash

# Configurações do Projeto Integrador III - Rede de Doações
PASSWORD_PADRAO = "doacao123"
TOTAL_JAN_ABR = 519
TOTAL_MAIO = 137
TOTAL_GERAL = TOTAL_JAN_ABR + TOTAL_MAIO

METAS_STATUS = {
    'available': 17,  # Doações Disponíveis para Recolhimento
    'claimed': 9,  # Doações Aguardando Confirmação
    'collected': TOTAL_GERAL - 26  # Restante como histórico (630 itens)
}

# Hubs Terrestres Reais para geolocalização variada no OpenLayers
HUBS_MUNDIAIS = [
    (-23.18, -45.96, "Jacarei, SP"),
    (-18.85, -41.94, "Governador Valadares, MG"),
    (-23.55, -46.63, "Sao Paulo, Brasil"),
    (40.71, -74.00, "New York, USA"),
    (48.85, 2.35, "Paris, France"),
    (35.68, 139.76, "Tokyo, Japan"),
    (-26.20, 28.04, "Johannesburg, South Africa"),
    (-33.86, 151.20, "Sydney, Australia"),
    (51.50, -0.12, "London, UK")
]


def gerar_localizacao():
    """Gera endereços não padronizados e coordenadas em terra firme."""
    lat_b, lon_b, local = random.choice(HUBS_MUNDIAIS)
    prefixo = random.choice(['Rua', 'Avenida', 'Alameda', 'Travessa', 'Street', 'Rue'])
    nome = random.choice(['das Flores', 'da Paz', 'Central', 'dos Herois', 'do Sol', 'da Liberdade'])
    numero = random.randint(1, 2500)

    # Adiciona um pequeno desvio para espalhar os pontos na cidade
    lat = lat_b + random.uniform(-0.15, 0.15)
    lon = lon_b + random.uniform(-0.15, 0.15)
    address = f"{prefixo} {nome}, {numero}, {local}"
    return lat, lon, address


def gerar_data_senoidal(mes_inicio, mes_fim, ano=2026):
    """Cria o efeito ondulado no gráfico do dashboard."""
    inicio = datetime(ano, mes_inicio, 1)
    # Define o fim do período (último dia do mês final)
    if mes_fim == 4:
        fim = datetime(ano, 4, 30)
    else:
        fim = datetime(ano, 5, 31)

    delta_dias = (fim - inicio).days
    while True:
        dia = random.randint(0, delta_dias)
        # Probabilidade baseada em seno para ondulação
        if random.random() < (math.sin(dia / 7.0) + 1.1) / 2.1:
            return inicio + timedelta(days=dia)


def popular_banco():
    with app.app_context():
        print("Limpando banco de dados...")
        db.drop_all()
        db.create_all()

        senha_hash = generate_password_hash(PASSWORD_PADRAO)

        # 1. CADASTRO DOS 50 DOADORES (Mantendo Jiraya e outros conforme solicitado)
        nomes_doadores = [
            "Jaspion", "He-Man", "John Wick", "National Kid", "Jiraya",
            "Agostinho Carrara", "Seu Madruga", "Mussum", "Didi Moco", "Zacarias",
            "Hebe Camargo", "Faustao", "Capitao Caverna", "MacGyver", "RoboCop",
            "Rambo", "Rocky Balboa", "Sherlock Holmes", "Arsene Lupin", "Indiana Jones",
            "Doc Brown", "Marty McFly", "Vingador", "Mestre dos Magos", "She-Ra",
            "Lion-O", "Zorro", "Chapolin Colorado", "Chaves", "Sr. Barriga",
            "Dona Florinda", "Popeye", "Pica-Pau", "Bugs Bunny", "Daffy Duck",
            "Tom Cavalcante", "Chico Anysio", "Tiao Macale", "Costinha", "Batore",
            "Galo Cego", "Seu Jorge", "Tim Maia Ficticio", "Sidney Magal", "Gretchen",
            "Tony Stark", "Bruce Wayne", "Peter Parker", "Wolverine", "Gandalf"
        ]

        usuarios_doadores = []
        for nome in nomes_doadores:
            lat, lon, addr = gerar_localizacao()
            u = User(username=nome.lower().replace(" ", "_"),
                     email=f"{nome.lower().replace(' ', '.')}@ficcao.com",
                     password_hash=senha_hash, user_type="Doador",
                     address=addr, latitude=lat, longitude=lon)
            db.session.add(u)
            usuarios_doadores.append(u)

        # 2. CADASTRO DAS 20 INSTITUIÇÕES
        nomes_inst = [
            "Asilo Arkham", "Escola Xavier", "Orfanato Vila Sesamo", "Fundacao Stark",
            "Abrigo da Batcaverna", "Castelo de Grayskull Inst", "Hogwarts Social",
            "Conselho Jedi", "Toca do Gato", "Corporacao Capsula", "Planeta Diario",
            "Sede Caca Fantasmas", "Vila dos Smurfs", "Agencia Mystery Inc",
            "Instituto Xavier", "Hospital Greys Sloane", "Policia Metro City",
            "Cozinha Hells Kitchen", "Laboratorios Star", "Sanatorio Silent Hill"
        ]

        usuarios_inst = []
        for nome in nomes_inst:
            lat, lon, addr = gerar_localizacao()
            i = User(username=nome.lower().replace(" ", "_"),
                     email=f"contato@{nome.lower().replace(' ', '.')}.org",
                     password_hash=senha_hash, user_type="Instituição",
                     address=addr, latitude=lat, longitude=lon)
            db.session.add(i)
            usuarios_inst.append(i)

        db.session.commit()

        # 3. GERAÇÃO DAS 656 DOAÇÕES
        print(f"Semeando {TOTAL_GERAL} doações...")
        itens = ["Arroz (5kg)", "Feijao (1kg)", "Macarrao", "Leite em Po", "Cesta Básica", "Oleo", "Cafe", "Gelatina"]

        for i in range(1, TOTAL_GERAL + 1):
            # Define o status conforme as metas
            if i <= METAS_STATUS['available']:
                status = 'available'
                inst_id = None
            elif i <= (METAS_STATUS['available'] + METAS_STATUS['claimed']):
                status = 'claimed'
                inst_id = random.choice(usuarios_inst).id
            else:
                status = 'collected'
                inst_id = random.choice(usuarios_inst).id

            # Seleciona doador e gera localização
            doador = random.choice(usuarios_doadores)
            lat, lon, addr = gerar_localizacao()

            # Lógica de Datas: IDs até 519 (Jan-Abr), IDs acima (Maio)
            if i <= TOTAL_JAN_ABR:
                data_criacao = gerar_data_senoidal(1, 4)
            else:
                data_criacao = gerar_data_senoidal(5, 5)

            db.session.add(Donation(
                description=random.choice(itens),
                quantity=f"{random.randint(1, 12)} un",
                status=status,
                user_id=doador.id,
                address=addr,
                latitude=lat,
                longitude=lon,
                claimed_by_id=inst_id,
                created_at=data_criacao
            ))

        db.session.commit()
        print(f"Sucesso! Banco populado com {TOTAL_GERAL} doações distribuídas globalmente.")


if __name__ == "__main__":
    popular_banco()