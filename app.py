from flask import Flask, request, render_template, redirect, url_for, flash, session
import pymysql

app = Flask(__name__)
app.secret_key = 'w6q&uUp0MBhst.hVvf|!jgh9Z?/mTZ3d'

# Configurações do banco de dados
db6_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'root',
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
    if session.get('username') != username:
        return render_template('erro.html')    

    user_id = session.get('user_id')    
    
    cursor = db6.cursor()
    # Select para ver as receitas do usuário que está logado
    cursor.execute("SELECT * FROM receitas WHERE user_id = %s", (user_id,))
    user_receita = cursor.fetchall()

    # Select para ver as receitas de outros usuários da Comidaria
    cursor.execute("SELECT * FROM receitas WHERE user_id != %s", (user_id,))
    outro_user_receita = cursor.fetchall()

    cursor.close()
    
    print(f"Username: {username}")
    print(f"User ID: {user_id}")
    print(f"User Receitas: {user_receita}")

    return render_template('home.html', receita=user_receita, outro_user_receita=outro_user_receita)

@app.route('/post_receita', methods=['GET', 'POST'])
def post_receita():
    if request.method == 'POST':
        titulo = request.form['titulo']
        ingredientes = request.form['ingredientes']
        preparo = request.form['preparo']

        user_id = session.get('user_id')
        if user_id:
            cursor = db6.cursor()
            cursor.execute("INSERT INTO receitas (user_id, titulo, ingredientes, preparo) VALUES (%s, %s, %s, %s)",
                           (user_id, titulo, ingredientes, preparo))
            db6.commit()
            cursor.close()            

            flash('Receita postada com sucesso!', 'success')
            return redirect(url_for('home', username=session.get('username')))

    return render_template('post_receita.html')

@app.route('/recipe/<int:recipe_id>', methods=['GET'])
def view_recipe(recipe_id):
    user_id = session.get('user_id')
    
    cursor = db6.cursor()
    cursor.execute("SELECT * FROM receitas WHERE id = %s", (recipe_id,))
    recipe = cursor.fetchone()
    cursor.close()
    
    if recipe:
        return render_template('recipe.html', recipe=recipe, is_owner=(user_id == recipe[0]))
    else:
        return render_template('erro.html')

@app.route('/edit_recipe/<int:recipe_id>', methods=['GET', 'POST'])
def edit_recipe(recipe_id):
    cursor = db6.cursor()
    cursor.execute("SELECT * FROM receitas WHERE user_id=%s", (recipe_id,))
    recipe = cursor.fetchone()
    cursor.close()

    if request.method == 'POST':
        titulo = request.form['titulo']
        ingredientes = request.form['ingredientes']
        preparo = request.form['preparo']

        cursor = db6.cursor()
        cursor.execute("UPDATE receitas SET titulo=%s, ingredientes=%s, preparo=%s WHERE user_id=%s",
                       (titulo, ingredientes, preparo, recipe_id))
        db6.commit()
        cursor.close()

        flash('Receita editada com sucesso!', 'success')
        return redirect(url_for('home', username=session.get('username')))

    return render_template('edit_recipe.html', recipe=recipe)


@app.route('/delete_recipe/<int:recipe_id>', methods=['POST'])
def delete_recipe(recipe_id):
    cursor = db6.cursor()
    cursor.execute("DELETE FROM receitas WHERE user_id=%s", (recipe_id,))
    db6.commit()
    cursor.close()

    flash('Receita excluída com sucesso!', 'success')
    return redirect(url_for('home', username=session.get('username')))


if __name__ == '__main__':
    app.run()