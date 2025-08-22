from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

# Configuración de la aplicación Flask
app = Flask(__name__)

# Función para conectar a la base de datos
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  # Deja la contraseña vacía por defecto
            database="control_vacunas"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error de conexión a la base de datos: {err}")
        return None

# Ruta principal para mostrar el formulario de registro
@app.route('/')
def index():
    return render_template('formulario.html')

# Ruta para manejar el envío del formulario
@app.route('/guardar_vacuna', methods=['POST'])
def guardar_vacuna():
    if request.method == 'POST':
        # Obtener los datos del formulario
        nombre = request.form['nombre']
        apellido_paterno = request.form['apellido_paterno']
        apellido_materno = request.form['apellido_materno']
        fecha_nacimiento = request.form['fecha_nacimiento']
        nombre_responsable = request.form['nombre_responsable']
        tipo_vacuna = request.form['tipo_vacuna']

        # Conectar a la base de datos e insertar los datos
        db = get_db_connection()
        if db:
            cursor = db.cursor()
            sql = "INSERT INTO vacunas_ninos (nombre, apellido_paterno, apellido_materno, fecha_nacimiento, nombre_responsable, tipo_vacuna) VALUES (%s, %s, %s, %s, %s, %s)"
            val = (nombre, apellido_paterno, apellido_materno, fecha_nacimiento, nombre_responsable, tipo_vacuna)
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()
            return redirect(url_for('index'))
    return "Hubo un error al guardar los datos."

# Ruta para mostrar los registros
@app.route('/vacunas')
def mostrar_vacunas():
    db = get_db_connection()
    vacunas = []
    if db:
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT id, nombre, apellido_paterno, fecha_nacimiento, tipo_vacuna FROM vacunas_ninos")
        vacunas = cursor.fetchall()
        cursor.close()
        db.close()
    return render_template('vacunas.html', vacunas=vacunas)

# ----------------- Funciones CRUD Adicionales -----------------

# Ruta para eliminar un registro
@app.route('/eliminar/<int:id>', methods=['GET'])
def eliminar_vacuna(id):
    db = get_db_connection()
    if db:
        cursor = db.cursor()
        sql = "DELETE FROM vacunas_ninos WHERE id = %s"
        cursor.execute(sql, (id,))
        db.commit()
        cursor.close()
        db.close()
    return redirect(url_for('mostrar_vacunas'))

# Ruta para mostrar el formulario de edición
@app.route('/editar/<int:id>', methods=['GET'])
def editar_vacuna(id):
    db = get_db_connection()
    vacuna = None
    if db:
        cursor = db.cursor(dictionary=True)
        sql = "SELECT * FROM vacunas_ninos WHERE id = %s"
        cursor.execute(sql, (id,))
        vacuna = cursor.fetchone()
        cursor.close()
        db.close()
    return render_template('editar.html', vacuna=vacuna)

# Ruta para guardar los cambios de un registro
@app.route('/actualizar_vacuna/<int:id>', methods=['POST'])
def actualizar_vacuna(id):
    if request.method == 'POST':
        # Obtener los datos del formulario de edición
        nombre = request.form['nombre']
        apellido_paterno = request.form['apellido_paterno']
        apellido_materno = request.form['apellido_materno']
        fecha_nacimiento = request.form['fecha_nacimiento']
        nombre_responsable = request.form['nombre_responsable']
        tipo_vacuna = request.form['tipo_vacuna']

        db = get_db_connection()
        if db:
            cursor = db.cursor()
            sql = "UPDATE vacunas_ninos SET nombre = %s, apellido_paterno = %s, apellido_materno = %s, fecha_nacimiento = %s, nombre_responsable = %s, tipo_vacuna = %s WHERE id = %s"
            val = (nombre, apellido_paterno, apellido_materno, fecha_nacimiento, nombre_responsable, tipo_vacuna, id)
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()
    return redirect(url_for('mostrar_vacunas'))

if __name__ == '__main__':
    app.run(debug=True)