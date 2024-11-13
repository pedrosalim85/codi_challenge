from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

cv_list = []
teste = 0
DATABASE = 'curriculos.db'

def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

# Função para criar a tabela de dados, se ela não existir
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

# Rota para criar a tabela de dados
@app.route('/initdb')
def initialize_database():
    init_db()
    return 'Database initialized'

@app.route('/')
def index():
    return render_template('index.html', cv_list=cv_list)


@app.route('/add', methods=['POST'])
def add():
    cv = {
        'Nome': request.form['nome'],
        'Sobrenome': request.form['sobrenome'],
        'Idade': request.form['idade'],
        'Formacao': request.form['formacao'],
        'Cidade': request.form['cidade'],
        'Habilidades': request.form['habilidades'],
        'Experiencia': request.form['experiencia']
    }
    cv_list.append(cv)
    return redirect(url_for('teste'))

@app.route('/teste')
def teste():
    return render_template('teste.html')

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
    

    cv_list[-1]['Teste'] = teste_pontos
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)