from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

DATABASE = 'C:/users/pedro/desktop/codi/challenge/codi_challenge/curriculos.db'

def get_db():
    db = sqlite3.connect(DATABASE)
    return db

@app.route('/')
def index():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM cv")
    cv_list = cursor.fetchall()
    db.close()
    return render_template('index.html', cv_list=cv_list)

@app.route('/add', methods=['POST'])
def add():
    nome = request.form['nome']
    sobrenome = request.form['sobrenome']
    idade = request.form['idade']
    formacao = request.form['formacao']
    cidade = request.form['cidade']
    habilidades = request.form['habilidades']
    experiencia = request.form['experiencia']

    cv = {
        'Nome': nome,
        'Sobrenome': sobrenome,
        'Idade': idade,
        'Formacao': formacao,
        'Cidade': cidade,
        'Habilidades': habilidades,
        'Experiencia': experiencia
    }
    cv_id = salvar_no_banco(cv)
    return redirect(url_for('teste', id=cv_id))

@app.route('/teste')
def teste():
    id = request.args.get('id')
    return render_template('teste.html', id=id)

@app.route('/respostas', methods=['POST'])
def respostas():
    teste_pontos = 0
    if request.form.get('pergunta1') == 'c':
        teste_pontos += 2
    if request.form.get('pergunta2') == 'a':
        teste_pontos += 2
    if request.form.get('pergunta3') == 'e':
        teste_pontos += 2
    if request.form.get('pergunta4') == 'b':
        teste_pontos += 2
    if request.form.get('pergunta5') == 'd':
        teste_pontos += 2

    id = buscar_ultimo_id()
    print(f"ID: {id}, Pontos do teste: {teste_pontos}") 
    atualizar_teste_no_banco(id, teste_pontos)
    return redirect(url_for('index'))

def salvar_no_banco(cv):
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute('''
        INSERT INTO cv (nome, sobrenome, idade, formacao, habilidades, cidade, experiencia, resultado_teste)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (cv['Nome'], cv['Sobrenome'], cv['Idade'], cv['Formacao'], cv['Habilidades'], cv['Cidade'], cv['Experiencia'], 0))
    
    db.commit()
    cv_id = cursor.lastrowid 
    db.close()
    print('Dados salvos no banco de dados.')
    return cv_id

def atualizar_teste_no_banco(id, teste_pontos):
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute('''
        UPDATE cv
        SET resultado_teste = ?
        WHERE id = ?
    ''', (teste_pontos, id))
    
    db.commit()
    db.close()
    print('Resultado do teste atualizado no banco de dados.')

def buscar_ultimo_id():
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute('SELECT MAX(id) FROM cv')
    ultimo_id = cursor.fetchone()[0]
    #ultimo_id = cursor.execute('SELECT MAX(id) FROM cv')
    
    db.close()
    return ultimo_id

if __name__ == '__main__':
    app.run(debug=True)
