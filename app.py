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

# **NUEVA RUTA para mostrar los registros**
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

if __name__ == '__main__':
    app.run(debug=True)