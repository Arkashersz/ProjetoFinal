from flask import Flask, send_from_directory, request, render_template, redirect, url_for, flash, session
import pymysql
import os
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.secret_key = 'w6q&uUp0MBhst.hVvf|!jgh9Z?/mTZ3d'

UPLOAD_FOLDER = 'static/upload'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Configurações do banco de dados
db6_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'admin',
    'database': 'comidaria',
    'port': 3306
}

db6 = pymysql.connect(**db6_config)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
    cursor.execute("SELECT post_id, titulo, ingredientes, preparo, imagem FROM receitas WHERE user_id = %s", (user_id,))
    user_receita = cursor.fetchall()

    cursor.execute("SELECT post_id, titulo, ingredientes, preparo, imagem FROM receitas WHERE user_id != %s", (user_id,))
    outro_user_receita = cursor.fetchall()

    cursor.close()
    
    return render_template('home.html', receita=user_receita, outro_user_receita=outro_user_receita, is_owner=lambda x: x[0] == user_id, os=os)

@app.route('/upload_image/<int:post_id>', methods=['POST'])
def upload_image(post_id):
    if 'file' not in request.files:
        flash('Nenhum arquivo enviado')
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        flash('Nenhum arquivo selecionado')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Atualize a receita no banco de dados com o caminho da imagem
        cursor = db6.cursor()
        cursor.execute("UPDATE receitas SET imagem=%s WHERE post_id=%s", (filepath, post_id))
        db6.commit()
        cursor.close()

        flash('Imagem enviada com sucesso!', 'success')
    else:
        flash('Extensão de arquivo não permitida', 'danger')

    return redirect(url_for('view_recipe', post_id=post_id))

@app.route('/uploads/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/post_receita', methods=['GET', 'POST'])
def post_receita():
    if request.method == 'POST':
        titulo = request.form['titulo']
        ingredientes = request.form['ingredientes']
        preparo = request.form['preparo']
        imagem = request.files['imagem']

        user_id = session.get('user_id')

        cursor = db6.cursor()

        if imagem and allowed_file(imagem.filename):
            filename = secure_filename(imagem.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            imagem.save(filepath)

            cursor.execute("INSERT INTO receitas (user_id, titulo, ingredientes, preparo, imagem) VALUES (%s, %s, %s, %s, %s)",
                           (user_id, titulo, ingredientes, preparo, filename))
        else:
            # Forneça um valor padrão (pode ser NULL) para o campo imagem
            cursor.execute("INSERT INTO receitas (user_id, titulo, ingredientes, preparo, imagem) VALUES (%s, %s, %s, %s, NULL)",
                           (user_id, titulo, ingredientes, preparo))

        db6.commit()
        cursor.close()

        flash('Receita postada com sucesso!', 'success')
        return redirect(url_for('home', username=session.get('username')))

    return render_template('post_receita.html')


@app.route('/recipe/<int:post_id>', methods=['GET'])
def view_recipe(post_id):
    if 'user_id' not in session:
        return render_template('erro.html')

    user_id = session['user_id']

    cursor = db6.cursor()
    cursor.execute("SELECT post_id, titulo, ingredientes, preparo, imagem FROM receitas WHERE post_id = %s", (post_id,))
    recipe = cursor.fetchone()
    cursor.close()

    if recipe:
        is_owner = (user_id == recipe[0])
        return render_template('recipe.html', recipe=recipe, is_owner=is_owner)
    else:
        return render_template('erro.html')


@app.route('/edit_recipe/<int:post_id>', methods=['GET', 'POST'])
def edit_recipe(post_id):
    cursor = db6.cursor()
    cursor.execute("SELECT * FROM receitas WHERE post_id=%s", (post_id,))
    recipe = cursor.fetchone()
    cursor.close()

    if request.method == 'POST':
        titulo = request.form['new_title']
        ingredientes = request.form['new_ingredients']
        preparo = request.form['new_instructions']

        cursor = db6.cursor()
        cursor.execute("UPDATE receitas SET titulo=%s, ingredientes=%s, preparo=%s WHERE post_id=%s",
                       (titulo, ingredientes, preparo, post_id))
        db6.commit()
        cursor.close()

        flash('Receita editada com sucesso!', 'success')
        return redirect(url_for('home', username=session.get('username')))

    return render_template('edit_recipe.html', recipe=recipe)




@app.route('/delete_recipe/<int:post_id>', methods=['POST'])
def delete_recipe(post_id):
    print(f"DEBUG: post_id recebido na rota delete_recipe: {post_id}")
    cursor = db6.cursor()
    cursor.execute("DELETE FROM receitas WHERE post_id=%s", (post_id,))
    db6.commit()
    cursor.close()

    flash('Receita excluída com sucesso!', 'success')
    return redirect(url_for('home', username=session.get('username')))




if __name__ == '__main__':
    app.run()