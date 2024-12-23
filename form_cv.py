import json
import os

print('Bemvindo ao cadastro de candidatos')

nome = input('Nome do candidato: ')
sobrenome = input('Sobrenome do candidato: ')
idade = input('Idade: ')
formacao = input('Formação superior: ')
cidade = input('Cidade de residência: ')

habilidades = []
lista = True

print('Adicione suas habilidades, confirmando cada uma com a tecla enter.')
print('Quando terminar, digite fim e confirme')

while lista:
    hab = input('habilidade: ')
    habilidades.append(hab)
    if hab == 'fim':
        habilidades.pop()
        lista = False

print('Adicione suas experiências profissionais, confirmando cada uma com a tecla enter.') 
print('Quando terminar, digite fim e confirme')

experiencia = []
lista2 = True

while lista2:
    exp = input('Experiência: ')
    experiencia.append(exp)
    if exp == 'fim':
        experiencia.pop()
        lista2 = False

print('Vamos agora realizar um teste cultural de acordo com os valores da empresa.')

teste = []

# Desenvolver o teste

curriculo = {'cv':{
                    'NOME':nome+' '+sobrenome,
                    'IDADE':idade,
                    'FORMACAO':formacao,
                    'HABILIDADES':habilidades,
                    'CIDADE':cidade,
                    'EXPERIENCIA':experiencia,
                    'RESULTADO_TESTE':teste
                   }   
}
def salvar_arquivo(dicionario, base_filename=f'curriculo', dir_path='.'):
    counter = 1
    filename = os.path.join(dir_path, f'{base_filename}_{counter}.json')
    while os.path.exists(filename):
        counter += 1
        filename = os.path.join(dir_path, f'{base_filename}_{counter}.json')

    with open(filename, 'w') as arquivo_json:
        json.dump(dicionario, arquivo_json, indent=4, ensure_ascii=False)

    print(f'Dicionário salvo em {filename}')

diretorio = 'C:/Users/Pedro/Desktop/Codi/challenge/cvs/'

salvar_arquivo(curriculo, dir_path=diretorio)