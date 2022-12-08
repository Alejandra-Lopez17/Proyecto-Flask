from flask import Flask, request, render_template, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = "mysecretkey"

# Mysql Settings
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_HOST'] =  '127.0.0.1' # l ocalhost
app.config['MYSQL_DB'] =  'flaskcrud'
app.config['MYSQL_PORT'] =  3308

# MySQL Connection
mysql = MySQL(app)

@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contactos')
    data = cur.fetchall()
    cur.close()
    return render_template('index.html', contactos=data)

@app.route('/agregar', methods=['POST'])
def agregar():
    if request.method == 'POST':
        nombres = request.form['nombres']
        apellidos = request.form['apellidos']
        correo = request.form['correo']
        materia = request.form['materia']
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO contactos (nombres, apellidos, correo, materia) VALUES (%s,%s,%s,%s)",
            (nombres, apellidos, correo, materia))
        mysql.connection.commit()
        return redirect(url_for('Index'))

@app.route('/editar/<id>', methods=['POST', 'GET'])
def editar(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contactos WHERE id = {0}'.format(id))
    data = cur.fetchall()
    cur.close()
    return render_template('editar.html', contacto=data[0])

@app.route('/actualizar/<id>', methods=['POST'])
def actualizar(id):
    if request.method == 'POST':
        nombres = request.form['nombres']
        apellidos = request.form['apellidos']
        correo = request.form['correo']
        materia = request.form['materia']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE contactos
            SET nombres = %s,
                correo = %s,
                apellidos = %s,
                materia = %s
            WHERE id = %s
        """, (nombres, correo, apellidos, materia, id))
        mysql.connection.commit()
        return redirect(url_for('Index'))

@app.route('/borrar/<id>', methods=['POST', 'GET'])
def borrar(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM contactos WHERE id = {0}'.format(id))
    mysql.connection.commit()
    return redirect(url_for('Index'))

app.run(debug=True)