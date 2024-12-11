import pandas as pd
import sqlite3

####### 1. DEFINIR OS CRITÉRIOS DA AVALIAÇÃO - VARIÁVEL RESPOSTA DO ML

def obter_informacoes_vaga():
    vaga = input('Qual a vaga que a empresa está oferecendo? ')
    numero_de_vagas = int(input('Quantas vagas são oferecidas? '))
    localizacao_empresa = input('Qual a cidade da vaga? ')
    formacao_req = input('Qual a formação exigida para a vaga? ')
    habilidades_req = input('Quais habilidades são requeridas? Separe por vírgulas. ').replace(" ", "").split(',')

    return vaga, numero_de_vagas, localizacao_empresa, formacao_req, habilidades_req


####### 2. PUXAR OS CURRÍCULOS DO BANCO DE DADOS 

DATABASE = 'C:/users/pedro/desktop/codi/challenge/codi_challenge/curriculos.db'

def get_db():
    db = sqlite3.connect(DATABASE)
    return db

def ler_curriculos():
    db = get_db() 
    query = "SELECT * FROM cv" 
    df = pd.read_sql_query(query, db) 
    db.close()

    df = df.dropna()

    return df


######## 3. AVALIAÇÃO DOS CANDIDATOS - MODELO DE MACHINE LEARNING SUPERVISIONADO

def avaliar_candidatos(candidatos_df, formacao_req, habilidades_req, localizacao_empresa, vaga):
    candidatos_df['PONTUACAO'] = 0

    candidatos_df['PONTUACAO'] += candidatos_df['FORMACAO'].str.contains(formacao_req).astype(int) * 10

    for habilidade in habilidades_req:
        candidatos_df['PONTUACAO'] += candidatos_df['HABILIDADES'].map(lambda x: 10 if habilidade in x else 0)
        
    candidatos_df['PONTUACAO'] += (candidatos_df['CIDADE'] == localizacao_empresa).astype(int)*10

    candidatos_df['PONTUACAO'] += candidatos_df['EXPERIENCIA'].str.contains(vaga).astype(int) * 10

    if (str(candidatos_df['EXPERIENCIA']) == vaga or vaga+'a'):
        candidatos_df['PONTUACAO'] += candidatos_df['ANOS']*1.5

    candidatos_df['PONTUACAO'] += candidatos_df['RESULTADO_TESTE']

    ###### COMPRIMIR A PONTUAÇÃO PARA REDUZIR AS DIFERENÇAS

    candidatos_df['PONTUACAO'].apply(lambda x: candidatos_df['PONTUACAO']/candidatos_df['PONTUACAO'].max())

    return candidatos_df.sort_values(by='PONTUACAO', ascending=False)

######### SISTEMA GERAL COM TODAS AS FUNÇÕES

def sistema_ats():
    vaga, numero_de_vagas, localizacao_empresa, formacao_req, habilidades_req = obter_informacoes_vaga()
    
    candidatos_df = ler_curriculos()
    print(candidatos_df)    ### MOSTRA TODOS OS CANDIDATOS CADASTRADOS NO DATABASE

    candidatos_avaliados = avaliar_candidatos(candidatos_df, formacao_req, habilidades_req, localizacao_empresa, vaga)
    
    print(f'Os candidatos aprovados para a vaga de {vaga} são:')
    print(candidatos_avaliados[['NOME', 'PONTUACAO']].head(numero_de_vagas))


sistema_ats()


