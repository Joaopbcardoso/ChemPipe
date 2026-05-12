CREATE TABLE IF NOT EXISTS AMOSTRA (
    id_amostra SERIAL PRIMARY KEY,
    codigo_amostra VARCHAR(50) UNIQUE NOT NULL,
    experimento VARCHAR(50) NOT NULL,
    replica INTEGER DEFAULT 1 CHECK (replica >= 1)
);

CREATE TABLE IF NOT EXISTS ABUNDANCIA (
    id_abundancia SERIAL PRIMARY KEY,
    intensidade NUMERIC CHECK (intensidade >= 0),
    id_amostra INTEGER NOT NULL REFERENCES AMOSTRA(id_amostra)
);

CREATE TABLE IF NOT EXISTS SINAL_ANALITICO (
    id_sinal_analitico SERIAL PRIMARY KEY,
    rotulo_composto VARCHAR(100),
    razao_mz NUMERIC NOT NULL,
    massa_neutra NUMERIC,
    tempo_retencao NUMERIC,
    largura_pico NUMERIC,
    id_abundancia INTEGER NOT NULL REFERENCES ABUNDANCIA(id_abundancia)
);

CREATE TABLE IF NOT EXISTS COMPOSTO (
    id_composto SERIAL PRIMARY KEY,
    identificador_composto VARCHAR(100) UNIQUE NOT NULL,
    formula_quimica VARCHAR(100),
    descricao TEXT,
    massa_neutra NUMERIC,
    link_referencia TEXT
);

CREATE TABLE IF NOT EXISTS CLASSE_QUIMICA (
    id_classe_quimica SERIAL PRIMARY KEY,
    nome_classe VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS COMPOSTO_CLASSE (
    id_composto INTEGER,
    id_classe_quimica INTEGER,
    PRIMARY KEY (id_composto, id_classe_quimica),
    FOREIGN KEY (id_composto) REFERENCES COMPOSTO(id_composto),
    FOREIGN KEY (id_classe_quimica) REFERENCES CLASSE_QUIMICA(id_classe_quimica)
);

CREATE TABLE IF NOT EXISTS IDENTIFICACAO (
    id_identificacao SERIAL PRIMARY KEY,
    pontuacao_total NUMERIC,
    pontuacao_fragmentacao NUMERIC,
    erro_massa_ppm NUMERIC,
    similaridade_isotopica NUMERIC,
    id_sinal_analitico INTEGER NOT NULL REFERENCES SINAL_ANALITICO(id_sinal_analitico),
    id_composto INTEGER NOT NULL REFERENCES COMPOSTO(id_composto)
);

CREATE TABLE IF NOT EXISTS ADUTO (
    id_aduto SERIAL PRIMARY KEY,
    tipo_aduto VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS IDENTIFICACAO_ADUTO (
    id_identificacao INTEGER,
    id_aduto INTEGER,
    PRIMARY KEY (id_identificacao, id_aduto),
    FOREIGN KEY (id_identificacao) REFERENCES IDENTIFICACAO(id_identificacao),
    FOREIGN KEY (id_aduto) REFERENCES ADUTO(id_aduto)
);



-- Contagem
SELECT COUNT(*) AS total_amostras FROM AMOSTRA;
SELECT COUNT(*) AS total_compostos FROM COMPOSTO;

-- Compostos por amostra
SELECT A.codigo_amostra, C.identificador_composto, SA.razao_mz, AB.intensidade
FROM AMOSTRA A
JOIN ABUNDANCIA AB ON A.id_amostra = AB.id_amostra
JOIN SINAL_ANALITICO SA ON AB.id_abundancia = SA.id_abundancia
JOIN IDENTIFICACAO I ON SA.id_sinal_analitico = I.id_sinal_analitico
JOIN COMPOSTO C ON I.id_composto = C.id_composto;
