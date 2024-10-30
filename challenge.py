import pandas as pd
import os
import glob

# REQUERIMENTOS DA EMPRESA
# pensar se não é melhor construir uma lista, do que uma string

print('Qual a vaga que a empresa está oferecendo?')
vaga = input()

print('Quantas vagas são oferecidas')
numero_de_vagas = input()

print('Qual a cidade da vaga?')
localizacao_empresa = input()

print('Qual as formação exigida para a vaga?')
formacao_req = input()

print('Quais habilidades são requeridas?')
habilidades_req = input()

# Leitura dos currículos
# Pensar em qual formato eles vão estar (json, csv, xml, doc)

arquivos = 'C:/caminho/'
curriculos = glob.glob(os.path.join(arquivos, "*.formato_do_curriculo"))

# Formatação dos dados dos candidatos
# desenvolver o tratamento dos dados para determinado formato

candidatos_cv = [] # lista de dataframes com os candidatos

# exemplo caso seja json

for candidato in curriculos:

  dado = pd.read_json(candidato)
  records = dado['cv']

  records_data = [] 
  for record in records: 
    record_data = [
      record['NOME'],
      record['IDADE'], 
      record['FORMACAO'], 
      record['HABILIDADES'],
      record['CIDADE'],
      record['EXPERIENCIA'],
      record['RESULTADO_TESTE'],
      ]
    records_data.append(record_data) 

  colunas = ['NOME', 'IDADE', 'FORMACAO', 'HABILIDADES', 'CIDADE', 'EXPERIENCIA', 'RESULTADO_TESTE']
  df = pd.DataFrame(records_data, columns=colunas)
  candidatos_cv.append(df)

candidatos_df = pd.concat(candidatos_cv, ignore_index=True)  # concatena cada dataframe de cada candidato em um dataframe geral

candidatos_df['PONTUACAO'] = [] #cria uma coluna para ir colocando a pontuação do candidato

# CRIAR O TESTE

# AVALIAÇÃO
# será que usa o mesmo dataframe ou cria um novo para os avaliados?

for candidato in candidatos_df.iterrows():

    pontos = 0

    candidatos_df['FORMACAO'] = candidatos_df['FORMACAO'].str.contains(formacao_req) # cria uma coluna com valores booleanos se a formacao estiver la

    # AVALIAR AS HABILIDADES DO CANDIDATO

    # AVALIAR A LOCALIZACAO DO CANDIDATO

    # AVALIAR O CANDIDATO PELAS RESPOSTAS DO TESTE NO DF


candidatos_df.sort_values('PONTUACAO')

print('Os candidatos aprovados são')
print(candidatos_df['NOME'].head(numero_de_vagas))