from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
cv_list = []
teste = 0

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