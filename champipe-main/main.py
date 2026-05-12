import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('sqlite:///chempipe.db')
df_abund = pd.read_excel('xlsx/ABUND.xlsx')
df_compostos = pd.read_excel('xlsx/Compostos_final.xlsx')
df_identificacao = pd.read_excel('xlsx/IDENTIFICACAO.xlsx')

df_abund.to_sql('abund', con=engine, if_exists='replace', index=False, method='multi')
df_compostos.to_sql('compostos', con=engine, if_exists='replace', index=False, method='multi')
df_identificacao.to_sql('identificacao', con=engine, if_exists='replace', index=False, method='multi')

print("ABUND:", df_abund.head())
print("COMPOSTOS:", df_compostos.head())
print("IDENTIFICACAO:", df_identificacao.head())
print("banco criado 'chempipe.db'")