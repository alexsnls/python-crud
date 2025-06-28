# Importacao de Biblioteca
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

# Configuracao do Flask e Banco de Dados
app = Flask(__name__)
DB = 'produtos.db'

# Inicializa o banco de dados
def init_db():
    with sqlite3.connect(DB) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS produtos (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            nome TEXT NOT NULL,
                            preco REAL NOT NULL,
                            quantidade INTEGER NOT NULL,
                            subtotal REAL NOT NULL
                        )''')
init_db()

# Rotas do Flask
@app.route('/')
def index():
    with sqlite3.connect(DB) as conn:
        cursor = conn.execute("SELECT * FROM produtos ORDER BY id DESC")
        produtos = cursor.fetchall()
    return render_template('index.html', produtos=produtos)

# Rota para criar um novo produto
@app.route('/criar', methods=['GET', 'POST'])
def criar():
    if request.method == 'POST':
        nome = request.form['nome']
        preco = float(request.form['preco'])
        quantidade = int(request.form['quantidade'])
        subtotal = preco * quantidade
        with sqlite3.connect(DB) as conn:
            conn.execute("INSERT INTO produtos (nome, preco, quantidade, subtotal) VALUES (?, ?, ?, ?)",
                         (nome, preco, quantidade, subtotal))
        return redirect(url_for('index'))  
    
    return render_template('criar.html')  

# Rota para editar um produto
@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    if request.method == 'POST':
        nome = request.form['nome']
        preco = float(request.form['preco'])
        quantidade = int(request.form['quantidade'])
        subtotal = preco * quantidade
        with sqlite3.connect(DB) as conn:
            conn.execute("UPDATE produtos SET nome=?, preco=?, quantidade=?, subtotal=? WHERE id=?",
                         (nome, preco, quantidade, subtotal, id))
        return redirect(url_for('index'))
    else:
        with sqlite3.connect(DB) as conn:
            cursor = conn.execute("SELECT * FROM produtos WHERE id=?", (id,))
            produto = cursor.fetchone()
        return render_template('editar.html', produto=produto)

# Rota para deletar um produto
@app.route('/deletar/<int:id>')
def deletar(id):
    with sqlite3.connect(DB) as conn:
        conn.execute("DELETE FROM produtos WHERE id=?", (id,))
    return redirect(url_for('index'))

# Rota para pesquisar produtos
@app.route('/pesquisar', methods=['GET'])
def pesquisar():
    termo = request.args.get('q', '')
    with sqlite3.connect(DB) as conn:
        cursor = conn.execute(
            "SELECT * FROM produtos WHERE nome LIKE ? ORDER BY id DESC",
            (f'%{termo}%',)
        )
        produtos = cursor.fetchall()
    return render_template('index.html', produtos=produtos, termo=termo)

# Rodar Aplicacao
if __name__ == '__main__':
    app.run(debug=True)
