from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.secret_key = 'mysecretekey'

users = {
    'usuario1': 'contraseña1',
    'usuario2': 'contraseña2',
}

# mysql connection configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'auro'
mysql = MySQL(app)

# --------------------------------------------------#
@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM usuarios')
    data = cur.fetchall()
    return render_template('index.html', usuarios=data)


#----------------------mod proyectos--------------------------------#

@app.route('/mod_proyectos.html')
def mod_proyectos():
    return render_template('mod_proyectos.html')


# Página de login
@app.route('/login.html', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        cur = mysql.connection.cursor()
        
        # Buscar en la tabla de aprendices
        cur.execute('SELECT * FROM aprendices WHERE usuario_aprendiz = %s', [username])
        user_aprendiz_row = cur.fetchone()
        if user_aprendiz_row:
            # Convertir la fila en un diccionario
            column_names = [desc[0] for desc in cur.description]  # Obtener nombres de columnas
            user_aprendiz = dict(zip(column_names, user_aprendiz_row))
            
            if user_aprendiz and check_password_hash(user_aprendiz['contrasena_aprendiz'], password):
                session['user_id'] = user_aprendiz['num_documento']
                session['username'] = user_aprendiz['usuario_aprendiz']
                flash('¡Inicio de sesión exitoso como aprendiz!')
                return redirect(url_for('index'))
            else:
                flash('Usuario no encontrado o contraseña incorrecta')
        else:
            # Buscar en la tabla de solicitantes si no se encuentra en aprendices
            cur.execute('SELECT * FROM solicitantes WHERE usuario_solicitante = %s', [username])
            user_solicitante_row = cur.fetchone()
            if user_solicitante_row:
                # Convertir la fila en un diccionario
                column_names = [desc[0] for desc in cur.description]  # Obtener nombres de columnas
                user_solicitante = dict(zip(column_names, user_solicitante_row))
                
                if user_solicitante and check_password_hash(user_solicitante['contrasena_solicitante'], password):
                    session['user_id'] = user_solicitante['num_documento']
                    session['username'] = user_solicitante['usuario_solicitante']
                    flash('¡Inicio de sesión exitoso como solicitante!')
                    return render_template ('index.html')
                else:
                    flash('Usuario no encontrado o contraseña incorrecta')
            else:
                flash('Usuario no encontrado o contraseña incorrecta')

    return render_template('login.html')

#--------------- registrarse ---------------#

@app.route ('/registrarse.html')
def registro_usuario ():
    return render_template('registrarse.html')

@app.route ('/add_usuario', methods = ['POST'])
def registro_un_usuario ():
    if request.method == 'POST':
        num_documento = request.form ['num_documento']
        nombre_usuario = request.form ['nombre_usuario']
        usuario_usuario = request.form ['usuario_usuario']
        telefono_usuario = request.form ['telefono_usuario']
        correo_usuario = request.form ['correo_usuario']
        contrasena_usuario = request.form ['contrasena_usuario']
        
        
        cur= mysql.connection.cursor()
        cur.execute('INSERT INTO usuarios (num_documento, nombre_usuario, usuario_usuario, telefono_usuario, correo_usuario, contrasena_usuario) VALUES (%s, %s, %s, %s, %s, %s)',
                    (num_documento,nombre_usuario,usuario_usuario,telefono_usuario, correo_usuario, contrasena_usuario))
        
        mysql.connection.commit()
        
        return render_template ('index.html')


#----------- Mod aprendiz --------------#

@app.route ('/mod_aprendiz.html')
def mod_aprendiz ():
    return render_template ('mod_aprendiz.html')



#----------- mod portafoleo -----------#

@app.route ('/mod_portafoleo.html')
def mod_aportafoleo ():
    return render_template ('mod_portafoleo.html')

if __name__ == '__main__':
    app.run(debug=True)