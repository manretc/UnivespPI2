-- 1. CRIAR E LIMPAR TABELAS
CREATE TABLE IF NOT EXISTS "user" (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(256),
    user_type VARCHAR(50) NOT NULL,
    address VARCHAR(200),
    latitude FLOAT,
    longitude FLOAT
);

CREATE TABLE IF NOT EXISTS donation (
    id SERIAL PRIMARY KEY,
    description VARCHAR(255) NOT NULL,
    quantity VARCHAR(50) NOT NULL,
    status VARCHAR(20) DEFAULT 'available',
    user_id INTEGER NOT NULL REFERENCES "user"(id),
    address VARCHAR(200) NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    claimed_by_id INTEGER REFERENCES "user"(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

BEGIN;

-- 2. CADASTRO DOS 50 DOADORES (Mantendo as suas correções: jiraya, etc)
TRUNCATE TABLE donation, "user" RESTART IDENTITY CASCADE;

INSERT INTO "user" (username, email, password_hash, user_type, address, latitude, longitude)
VALUES
('jaspion', 'jaspion@ficcao.com', 'scrypt:32768:8:1$7fM3I5n4vQkL', 'Doador', 'Rua Galactica, 101', -23.18, -45.96),
('he_man', 'heman@ficcao.com', 'scrypt:32768:8:1$7fM3I5n4vQkL', 'Doador', 'Castelo de Grayskull', -23.55, -46.63),
('john_wick', 'john_wick@ficcao.com', 'scrypt:32768:8:1$7fM3I5n4vQkL', 'Doador', 'Continental Hotel', 40.71, -74.00),
('national_kid', 'national_kid@ficcao.com', 'scrypt:32768:8:1$7fM3I5n4vQkL', 'Doador', 'Tokyo Tower', 35.68, 139.76),
('jiraya', 'jiraya@ficcao.com', 'scrypt:32768:8:1$7fM3I5n4vQkL', 'Doador', 'Mansao Yamaji', 34.69, 135.50),
('agostinho_carrara', 'agostinho@ficcao.com', 'scrypt:32768:8:1$7fM3I5n4vQkL', 'Doador', 'Rua do Beco, 14', -22.90, -43.17),
('seu_madruga', 'madruga@ficcao.com', 'scrypt:32768:8:1$7fM3I5n4vQkL', 'Doador', 'Vila do Chaves, 72', 19.43, -99.13),
('mussum', 'mussum@ficcao.com', 'scrypt:32768:8:1$7fM3I5n4vQkL', 'Doador', 'Morro da Mangueira', -22.90, -43.23),
('didi_moco', 'didi_moco@ficcao.com', 'scrypt:32768:8:1$7fM3I5n4vQkL', 'Doador', 'Rua dos Trapalhoes', -23.00, -43.30),
('zacarias', 'zacarias@ficcao.com', 'scrypt:32768:8:1$7fM3I5n4vQkL', 'Doador', 'Bairro da Alegria', -19.92, -43.94),
('hebe_camargo', 'hebe@ficcao.com', 'scrypt:32768:8:1$7fM3I5n4vQkL', 'Doador', 'Av. Brasil, 88', -23.56, -46.68),
('faustao', 'faustao@ficcao.com', 'scrypt:32768:8:1$7fM3I5n4vQkL', 'Doador', 'Teatro Ficticio', -23.58, -46.67),
('capitao_caverna', 'caverna@ficcao.com', 'scrypt:32768:8:1$7fM3I5n4vQkL', 'Doador', 'Caverna Secreta', 36.16, -115.13),
('macgyver', 'macgyver@ficcao.com', 'scrypt:32768:8:1$7fM3I5n4vQkL', 'Doador', 'Lab Phoenix', 34.05, -118.24),
('robocop', 'robocop@ficcao.com', 'scrypt:32768:8:1$7fM3I5n4vQkL', 'Doador', 'DP Detroit', 42.33, -83.04),
('rambo', 'rambo@ficcao.com', 'scrypt:32768:8:1$7fM3I5n4vQkL', 'Doador', 'Acampamento Selva', 31.55, 35.10),
('rocky_balboa', 'rocky@ficcao.com', 'scrypt:32768:8:1$7fM3I5n4vQkL', 'Doador', 'Filadelfia', 39.95, -75.16),
('sherlock_holmes', 'sherlock@ficcao.com', 'scrypt:32768:8:1$7fM3I5n4vQkL', 'Doador', '221B Baker St', 51.52, -0.15),
('arsene_lupin', 'lupin@ficcao.com', 'scrypt:32768:8:1$7fM3I5n4vQkL', 'Doador', 'Palacio Paris', 48.85, 2.35),
('indiana_jones', 'indy@ficcao.com', 'scrypt:32768:8:1$7fM3I5n4vQkL', 'Doador', 'Museu Historia', 38.89, -77.03),
('doc_brown', 'doc@ficcao.com', 'scrypt:32768:8:1$7fM3I5n4vQkL', 'Doador', 'Hill Valley', 34.14, -118.33),
('marty_mcfly', 'marty@ficcao.com', 'scrypt:32768:8:1$7fM3I5n4vQkL', 'Doador', 'Rua do Futuro', 34.14, -118.34),
('vingador', 'vingador@ficcao.com', 'scrypt:32768:8:1$7fM3I5n4vQkL', 'Doador', 'Montanha Destino', 36.50, -114.70),
('mestre_dos_magos', 'mestre@ficcao.com', 'scrypt:32768:8:1$7fM3I5n4vQkL', 'Doador', 'Reino Encantado', 36.60, -114.80),
('she_ra', 'shera@ficcao.com', 'scrypt:32768:8:1$7fM3I5n4vQkL', 'Doador', 'Palacio Cristal', -23.40, -46.50),
('lion_o', 'lion@ficcao.com', 'scrypt:32768:8:1$7fM3I5n4vQkL', 'Doador', 'Toca dos Gatos', -26.20, 28.04),
('zorro', 'zorro@ficcao.com', 'scrypt:32768:8:1$7fM3I5n4vQkL', 'Doador', 'Hacienda Vega', 34.00, -118.50),
('chapolin_colorado', 'chapolin@ficcao.com', 'scrypt:32768:8:1$7fM3I5n4vQkL', 'Doador', 'Anteninha Vinil', 19.40, -99.10),
('chaves', 'chaves@ficcao.com', 'scrypt:32768:8:1$7fM3I5n4vQkL', 'Doador', 'Barril da Vila', 19.41, -99.11),
('sr_barriga', 'barriga@ficcao.com', 'scrypt:32768:8:1$7fM3I5n4vQkL', 'Doador', 'Imobiliaria', 19.42, -99.12),
('dona_florinda', 'florinda@ficcao.com', 'scrypt:32768:8:1$7fM3I5n4vQkL', 'Doador', 'Vila Casa 14', 19.44, -99.14),
('popeye', 'popeye@ficcao.com', 'scrypt:32768:8:1$7fM3I5n4vQkL', 'Doador', 'Cais do Porto', 42.36, -71.05),
('pica_pau', 'picapau@ficcao.com', 'scrypt:32768:8:1$7fM3I5n4vQkL', 'Doador', 'Arvore Parque', 34.00, -118.00),
('bugs_bunny', 'pernalonga@ficcao.com', 'scrypt:32768:8:1$7fM3I5n4vQkL', 'Doador', 'Buraco Coelho', 34.10, -118.30),
('daffy_duck', 'patolino@ficcao.com', 'scrypt:32768:8:1$7fM3I5n4vQkL', 'Doador', 'Lago Patos', 34.11, -118.31),
('tom_cavalcante', 'tom@ficcao.com', 'scrypt:32768:8:1$7fM3I5n4vQkL', 'Doador', 'Rua Imitacoes', -3.73, -38.52),
('chico_anysio', 'chico@ficcao.com', 'scrypt:32768:8:1$7fM3I5n4vQkL', 'Doador', 'Escolinha', -22.91, -43.22),
('tiao_macale', 'tiao@ficcao.com', 'scrypt:32768:8:1$7fM3I5n4vQkL', 'Doador', 'Ih Nojento', -22.92, -43.23),
('costinha', 'costinha@ficcao.com', 'scrypt:32768:8:1$7fM3I5n4vQkL', 'Doador', 'Rua Piada', -22.93, -43.24),
('batore', 'batore@ficcao.com', 'scrypt:32768:8:1$7fM3I5n4vQkL', 'Doador', 'Praca da Praca', -23.50, -46.60),
('galo_cego', 'galo@ficcao.com', 'scrypt:32768:8:1$7fM3I5n4vQkL', 'Doador', 'Rua Escuridao', -23.51, -46.61),
('seu_jorge', 'jorge@ficcao.com', 'scrypt:32768:8:1$7fM3I5n4vQkL', 'Doador', 'Ipanema', -22.98, -43.20),
('tim_maia_ficticio', 'tim@ficcao.com', 'scrypt:32768:8:1$7fM3I5n4vQkL', 'Doador', 'Vale de Tudo', -22.90, -43.20),
('sidney_magal', 'magal@ficcao.com', 'scrypt:32768:8:1$7fM3I5n4vQkL', 'Doador', 'Rua Cigano', -22.95, -43.25),
('gretchen', 'gretchen@ficcao.com', 'scrypt:32768:8:1$7fM3I5n4vQkL', 'Doador', 'Rua Rebolado', -23.60, -46.70),
('tony_stark', 'stark@ficcao.com', 'scrypt:32768:8:1$7fM3I5n4vQkL', 'Doador', 'Stark Tower', 40.75, -73.98),
('bruce_wayne', 'wayne@ficcao.com', 'scrypt:32768:8:1$7fM3I5n4vQkL', 'Doador', 'Wayne Manor', 40.70, -74.01),
('peter_parker', 'parker@ficcao.com', 'scrypt:32768:8:1$7fM3I5n4vQkL', 'Doador', 'Queens NY', 40.72, -73.84),
('wolverine', 'logan@ficcao.com', 'scrypt:32768:8:1$7fM3I5n4vQkL', 'Doador', 'Escola Xavier', 41.30, -73.70),
('gandalf', 'gandalf@ficcao.com', 'scrypt:32768:8:1$7fM3I5n4vQkL', 'Doador', 'Hobbiton', -37.81, 175.68);

-- 3. CADASTRO DAS 20 INSTITUIÇÕES
INSERT INTO "user" (username, email, password_hash, user_type, address, latitude, longitude)
VALUES
('asilo_arkham', 'contato@arkham.org', 'scrypt:32768:8:1$7fM3I5n4vQkL', 'Instituição', 'Gotham City', 40.73, -73.93),
('escola_xavier', 'contato@xavier.org', 'scrypt:32768:8:1$7fM3I5n4vQkL', 'Instituição', 'Westchester NY', 41.31, -73.71),
('orfanato_vila_sesamo', 'contato@sesamo.org', 'scrypt:32768:8:1$7fM3I5n4vQkL', 'Instituição', 'Sesame St', 40.78, -73.97),
('fundacao_stark', 'contato@stark.org', 'scrypt:32768:8:1$7fM3I5n4vQkL', 'Instituição', 'Stark Ind', 34.02, -118.49),
('abrigo_da_batcaverna', 'contato@batcave.org', 'scrypt:32768:8:1$7fM3I5n4vQkL', 'Instituição', 'Caverna', 40.69, -74.02),
('castelo_de_grayskull_inst', 'contato@grayskull.org', 'scrypt:32768:8:1$7fM3I5n4vQkL', 'Instituição', 'Eternia', -23.54, -46.62),
('hogwarts_social', 'contato@hogwarts.org', 'scrypt:32768:8:1$7fM3I5n4vQkL', 'Instituição', 'Highlands', 56.49, -4.20),
('conselho_jedi', 'contato@jedi.org', 'scrypt:32768:8:1$7fM3I5n4vQkL', 'Instituição', 'Coruscant', 34.05, -118.25),
('toca_do_gato', 'contato@thundercats.org', 'scrypt:32768:8:1$7fM3I5n4vQkL', 'Instituição', 'Third Earth', -26.21, 28.05),
('corporacao_capsula', 'contato@capsule.org', 'scrypt:32768:8:1$7fM3I5n4vQkL', 'Instituição', 'West City', 35.69, 139.75),
('planeta_diario', 'contato@planeta.org', 'scrypt:32768:8:1$7fM3I5n4vQkL', 'Instituição', 'Metropolis', 38.90, -77.04),
('sede_caca_fantasmas', 'contato@ghostbusters.org', 'scrypt:32768:8:1$7fM3I5n4vQkL', 'Instituição', 'North Moore St', 40.72, -74.00),
('vila_dos_smurfs', 'contato@smurfs.org', 'scrypt:32768:8:1$7fM3I5n4vQkL', 'Instituição', 'Cogumelo Verde', 50.85, 4.35),
('agencia_mystery_inc', 'contato@mystery.org', 'scrypt:32768:8:1$7fM3I5n4vQkL', 'Instituição', 'Coolsville', 39.10, -84.51),
('instituto_xavier', 'contato@instituto.org', 'scrypt:32768:8:1$7fM3I5n4vQkL', 'Instituição', 'Genosha', -23.19, -45.97),
('hospital_greys_sloane', 'contato@greys.org', 'scrypt:32768:8:1$7fM3I5n4vQkL', 'Instituição', 'Seattle', 47.60, -122.33),
('policia_metro_city', 'contato@metro.org', 'scrypt:32768:8:1$7fM3I5n4vQkL', 'Instituição', 'Centro Policial', 42.34, -83.05),
('cozinha_hells_kitchen', 'contato@hellskitchen.org', 'scrypt:32768:8:1$7fM3I5n4vQkL', 'Instituição', 'Hells Kitchen NY', 40.76, -73.99),
('laboratorios_star', 'contato@star.org', 'scrypt:32768:8:1$7fM3I5n4vQkL', 'Instituição', 'Central City', 38.62, -90.19),
('sanatorio_silent_hill', 'contato@silenthill.org', 'scrypt:32768:8:1$7fM3I5n4vQkL', 'Instituição', 'Foggy St', 44.00, -70.00)
ON CONFLICT (email) DO NOTHING;

COMMIT;

BEGIN;

-- 4. GERAR AS 656 DOAÇÕES (519 de Jan-Abr + 137 de Maio)
INSERT INTO donation (description, quantity, status, user_id, address, latitude, longitude, claimed_by_id, created_at)
SELECT
    -- Descrição aleatória do item
    (ARRAY['Arroz (5kg)', 'Feijao (1kg)', 'Macarrao', 'Leite em Po', 'Cesta Básica', 'Oleo', 'Cafe', 'Gelatina'])[floor(random() * 8 + 1)],

    -- Quantidade aleatória
    (floor(random() * 12 + 1) || ' un'),

    -- Status conforme a sua meta (17 disponíveis, 9 aguardando, restante concluídas)
    CASE
        WHEN s.id <= 17 THEN 'available'
        WHEN s.id <= 26 THEN 'claimed'
        ELSE 'collected'
    END,

    -- Doador aleatório (IDs 1 a 50)
    floor(random() * 50 + 1),

    -- GERAÇÃO DE ENDEREÇO NÃO PADRONIZADO
    (ARRAY['Rua', 'Avenida', 'Alameda', 'Travessa', 'Street', 'Rue', 'Boulevard', 'Avenida', 'Praca'])[floor(random() * 9 + 1)] || ' ' ||
    (ARRAY['das Flores', 'da Paz', 'Central', 'do Sol', 'dos Artistas', 'Galactica', 'dos Herois', 'do Futuro', 'Principal', 'da Liberdade', 'das Palmeiras', 'da Esperanca'])[floor(random() * 12 + 1)] || ', ' ||
    floor(random() * 2500 + 1),

    -- COORDENADAS TERRESTRES (Sorteio entre Hubs Mundiais)
    (ARRAY[-23.18, -18.85, -23.55, 40.71, 48.85, 35.68, -26.20, -33.86, 51.50])[h.hub_idx] + (random() * 0.4 - 0.2), -- Latitude
    (ARRAY[-45.96, -41.94, -46.63, -74.00, 2.35, 139.76, 28.04, 151.20, -0.12])[h.hub_idx] + (random() * 0.4 - 0.2), -- Longitude

    -- Instituição (IDs 51 a 70) apenas se não estiver disponível
    CASE
        WHEN s.id > 17 THEN floor(random() * 20 + 51)
        ELSE NULL
    END,

    -- Lógica de Datas: IDs até 519 (Jan-Abr), IDs de 520 a 656 (Maio)
    CASE
        WHEN s.id <= 519 THEN '2026-01-01'::timestamp + (random() * interval '119 days')
        ELSE '2026-05-01'::timestamp + (random() * interval '30 days')
    END

FROM generate_series(1, 656) AS s(id)
CROSS JOIN LATERAL (SELECT floor(random() * 9 + 1)::int AS hub_idx) AS h;

COMMIT;