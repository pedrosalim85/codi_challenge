import pandas as pd
import os
import glob
import numpy as np

DATABASE = 'curriculos.db'

def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

def obter_informacoes_vaga():
    vaga = input('Qual a vaga que a empresa está oferecendo? ')
    numero_de_vagas = int(input('Quantas vagas são oferecidas? '))
    localizacao_empresa = input('Qual a cidade da vaga? ')
    formacao_req = input('Qual a formação exigida para a vaga? ')
    habilidades_req = input('Quais habilidades são requeridas? Separe por vírgulas. ').replace(" ", "").split(',')
    return vaga, numero_de_vagas, localizacao_empresa, formacao_req, habilidades_req

def ler_curriculos(diretorio):
    arquivos = glob.glob(os.path.join(diretorio, '*.json'))
    candidatos_cv = []
    
    for arquivo in arquivos:
        dados = pd.read_json(arquivo, encoding='latin-1')

        records = dados['cv']
        
        record_data = [
                
            records['NOME'],
            records['IDADE'], 
            records['FORMACAO'], 
            records['HABILIDADES'],
            records['CIDADE'],
            records['EXPERIENCIA'],
            records['RESULTADO_TESTE'],
            ]
        candidatos_cv.append(record_data)

    colunas = ['NOME', 'IDADE', 'FORMACAO', 'HABILIDADES', 'CIDADE', 'EXPERIENCIA', 'RESULTADO_TESTE']    
    df = pd.DataFrame(candidatos_cv, columns=colunas)

    df = df.map(lambda x: np.nan if x == [] else x)
    df = df.dropna()

    return df

def avaliar_candidatos(candidatos_df, formacao_req, habilidades_req, localizacao_empresa, vaga):
    candidatos_df['PONTUACAO'] = 0
    
    candidatos_df['PONTUACAO'] += candidatos_df['FORMACAO'].str.contains(formacao_req).astype(int) * 10

    for habilidade in habilidades_req:
        candidatos_df['PONTUACAO'] += candidatos_df['HABILIDADES'].map(lambda x: 10 if habilidade in x else 0)
        
    candidatos_df['PONTUACAO'] += (candidatos_df['CIDADE'] == localizacao_empresa).astype(int)*10

    candidatos_df['PONTUACAO'] += candidatos_df['EXPERIENCIA'].str.contains(vaga).astype(int) * 10

    candidatos_df['PONTUACAO'] += candidatos_df['RESULTADO_TESTE']

    return candidatos_df.sort_values(by='PONTUACAO', ascending=False)

def sistema_ats():
    vaga, numero_de_vagas, localizacao_empresa, formacao_req, habilidades_req = obter_informacoes_vaga()
    
    diretorio = 'C:/users/pedro/desktop/codi/challenge/cvs/'
    candidatos_df = ler_curriculos(diretorio)
    print(candidatos_df)
    candidatos_avaliados = avaliar_candidatos(candidatos_df, formacao_req, habilidades_req, localizacao_empresa, vaga)
    
    print(f'Os candidatos aprovados para a vaga de {vaga} são:')
    print(candidatos_avaliados[['NOME', 'PONTUACAO']].head(numero_de_vagas))
   

sistema_ats()


