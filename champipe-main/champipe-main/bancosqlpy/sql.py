from sqlalchemy import (
    create_engine, MetaData, Table, Column,
    Integer, String, Text, Numeric, ForeignKey
)

# conecta direto no arquivo SQLite
engine = create_engine("sqlite:///chempipe.db")# pode tar errado nao fiz muitos testes :)

metadata = MetaData()

AMOSTRA = Table(
    "amostra", metadata,
    Column("id_amostra", Integer, primary_key=True),
    Column("codigo_amostra", String(50)),
    Column("experimento", String(50)),
    Column("replica", Integer)
)

ABUNDANCIA = Table(
    "abundancia", metadata,
    Column("id_abundancia", Integer, primary_key=True),
    Column("intensidade", Numeric),
    Column("id_amostra", Integer, ForeignKey("amostra.id_amostra"))
)

SINAL_ANALITICO = Table(
    "sinal_analitico", metadata,
    Column("id_sinal_analitico", Integer, primary_key=True),
    Column("rotulo_composto", String(100)),
    Column("razao_mz", Numeric),
    Column("massa_neutra", Numeric),
    Column("tempo_retencao", Numeric),
    Column("largura_pico", Numeric),
    Column("id_abundancia", Integer, ForeignKey("abundancia.id_abundancia"))
)

COMPOSTO = Table(
    "composto", metadata,
    Column("id_composto", Integer, primary_key=True),
    Column("identificador_composto", String(100)),
    Column("formula_quimica", String(100)),
    Column("descricao", Text),
    Column("massa_neutra", Numeric),
    Column("link_referencia", Text)
)

CLASSE_QUIMICA = Table(
    "classe_quimica", metadata,
    Column("id_classe_quimica", Integer, primary_key=True),
    Column("nome_classe", String(100))
)

COMPOSTO_CLASSE = Table(
    "composto_classe", metadata,
    Column("id_composto", Integer, ForeignKey("composto.id_composto"), primary_key=True),
    Column("id_classe_quimica", Integer, ForeignKey("classe_quimica.id_classe_quimica"), primary_key=True)
)

IDENTIFICACAO = Table(
    "identificacao", metadata,
    Column("id_identificacao", Integer, primary_key=True),
    Column("pontuacao_total", Numeric),
    Column("pontuacao_fragmentacao", Numeric),
    Column("erro_massa_ppm", Numeric),
    Column("similaridade_isotopica", Numeric),
    Column("id_sinal_analitico", Integer, ForeignKey("sinal_analitico.id_sinal_analitico")),
    Column("id_composto", Integer, ForeignKey("composto.id_composto"))
)

ADUTO = Table(
    "aduto", metadata,
    Column("id_aduto", Integer, primary_key=True),
    Column("tipo_aduto", String(50))
)

IDENTIFICACAO_ADUTO = Table(
    "identificacao_aduto", metadata,
    Column("id_identificacao", Integer, ForeignKey("identificacao.id_identificacao"), primary_key=True),
    Column("id_aduto", Integer, ForeignKey("aduto.id_aduto"), primary_key=True)
)

metadata.create_all(engine)
