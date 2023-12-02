from flask import Flask, request, render_template, redirect, url_for, flash, session
import pymysql

app = Flask(__name__)
app.secret_key = 'w6q&uUp0MBhst.hVvf|!jgh9Z?/mTZ3d'

# Configurações do banco de dados
db6_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'admin',
    'database': 'comidaria',
    'port': 3306
}



db6 = pymysql.connect(**db6_config)

def verificar_user(username):
    cursor = db6.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    cursor.close()
    return user is not None

def verificar_email(email):
    cursor = db6.cursor()
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    cursor.close()
    return user is not None


@app.route('/')
def pag_inicial():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    messages = []  # Inicializa uma lista para armazenar mensagens

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        if verificar_user(username):
            messages.append(('danger', 'Nome de usuário já está em uso. Por favor, escolha outro.'))

        if verificar_email(email):
            messages.append(('danger', 'E-mail já está em uso. Por favor, escolha outro.'))

        if not messages:
            cursor = db6.cursor()
            cursor.execute("INSERT INTO users (username, password, email) VALUES (%s, %s, %s)", (username, password, email))
            db6.commit()
            cursor.close()

            messages.append(('success', 'Você foi registrado com sucesso!'))
            return redirect(url_for('login'))

    return render_template('registro.html', messages=messages)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor = db6.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        cursor.close()
        if user:
            session['user_id'] = user[0]
            session['username'] = username
            # Depois de logado, redirecione para onde quiser
            return redirect('/home/' + user[1]) 
        else:
            flash('Login falhou. Verifique seu nome de usuário e senha.', 'danger')

    return render_template('login.html')

@app.route('/home/<username>', methods=['GET', 'POST'])
def home(username):
    print(session.get('username'))
    if(session.get('username') != username):
       return render_template('erro.html')
    return render_template('home.html')

if __name__ == '__main__':
    app.run()