from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

# Configuración de la aplicación Flask
app = Flask(__name__)

# Función para conectar a la nueva base de datos
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="control_vacunas_v2"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error de conexión a la base de datos: {err}")
        return None

# Rutas principales
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/niños')
def niños_modulo():
    db = get_db_connection()
    niños = []
    if db:
        cursor = db.cursor(dictionary=True)
        sql = """
            SELECT 
                n.id, 
                n.nombre, 
                n.apellido_paterno, 
                n.apellido_materno, 
                n.fecha_nacimiento,
                COUNT(va.id) AS total_vacunas
            FROM niños n
            LEFT JOIN vacunas_aplicadas va ON n.id = va.id_niño
            GROUP BY n.id
            ORDER BY n.id DESC
        """
        cursor.execute(sql)
        niños = cursor.fetchall()
        cursor.close()
        db.close()
    return render_template('niños.html', niños=niños)

# --- Funcionalidades para el Módulo de Niños ---

# Ruta para ELIMINAR un niño
@app.route('/eliminar_niño/<int:id>', methods=['GET'])
def eliminar_niño(id):
    db = get_db_connection()
    if db:
        cursor = db.cursor()
        sql = "DELETE FROM niños WHERE id = %s"
        cursor.execute(sql, (id,))
        db.commit()
        cursor.close()
        db.close()
    return redirect(url_for('niños_modulo'))

# Ruta para REVISAR la información y el historial de vacunas de un niño
@app.route('/niño/<int:id>')
def revisar_niño(id):
    db = get_db_connection()
    niño = None
    historial_vacunas = []
    if db:
        cursor = db.cursor(dictionary=True)
        
        # Consulta para obtener los datos del niño
        sql_niño = "SELECT * FROM niños WHERE id = %s"
        cursor.execute(sql_niño, (id,))
        niño = cursor.fetchone()

        # Consulta para obtener el historial de vacunas del niño, uniendo tablas
        sql_historial = """
            SELECT 
                va.fecha_aplicacion, 
                va.dosis, 
                tv.nombre AS tipo_vacuna, 
                pv.nombre AS personal_vacunador, 
                r.nombre AS nombre_responsable
            FROM vacunas_aplicadas va
            JOIN tipos_vacuna tv ON va.id_vacuna = tv.id
            JOIN personal_vacunador pv ON va.id_personal = pv.id
            JOIN responsables r ON va.id_responsable = r.id
            WHERE va.id_niño = %s
            ORDER BY va.fecha_aplicacion DESC
        """
        cursor.execute(sql_historial, (id,))
        historial_vacunas = cursor.fetchall()

        cursor.close()
        db.close()
    
    if niño is None:
        return "Niño no encontrado", 404
        
    return render_template('niño_detalle.html', niño=niño, historial=historial_vacunas)

# Ruta para mostrar el formulario de REGISTRO DE VACUNA
@app.route('/registrar_vacuna/<int:id>')
def registrar_vacuna_form(id):
    db = get_db_connection()
    niño = None
    tipos_vacuna = []
    personal = []
    responsables = []
    
    if db:
        cursor = db.cursor(dictionary=True)
        
        # Obtener los datos del niño para mostrarlos en el formulario
        sql_niño = "SELECT id, nombre, apellido_paterno FROM niños WHERE id = %s"
        cursor.execute(sql_niño, (id,))
        niño = cursor.fetchone()

        # Obtener los tipos de vacunas para el dropdown
        cursor.execute("SELECT id, nombre FROM tipos_vacuna ORDER BY nombre")
        tipos_vacuna = cursor.fetchall()

        # Obtener el personal para el dropdown
        cursor.execute("SELECT id, nombre FROM personal_vacunador ORDER BY nombre")
        personal = cursor.fetchall()
        
        # Obtener los responsables para el dropdown
        cursor.execute("SELECT id, nombre FROM responsables ORDER BY nombre")
        responsables = cursor.fetchall()
        
        cursor.close()
        db.close()
    
    if niño is None:
        return "Niño no encontrado", 404
    
    return render_template('registrar_vacuna_form.html', 
                           niño=niño, 
                           tipos_vacuna=tipos_vacuna, 
                           personal=personal,
                           responsables=responsables)


# Ruta para GUARDAR la nueva vacuna
@app.route('/guardar_vacuna_niño/<int:id_nino>', methods=['POST'])
def guardar_vacuna_niño(id_nino):
    if request.method == 'POST':
        id_responsable = request.form['id_responsable']
        id_vacuna = request.form['id_vacuna']
        id_personal = request.form['id_personal']
        fecha_aplicacion = request.form['fecha_aplicacion']
        dosis = request.form['dosis']
        
        db = get_db_connection()
        if db:
            cursor = db.cursor()
            sql = "INSERT INTO vacunas_aplicadas (id_niño, id_responsable, id_vacuna, id_personal, fecha_aplicacion, dosis) VALUES (%s, %s, %s, %s, %s, %s)"
            val = (id_niño, id_responsable, id_vacuna, id_personal, fecha_aplicacion, dosis)
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()
            
    return redirect(url_for('niños_modulo'))

# Rutas de otros módulos (sin cambios)
@app.route('/personal')
def personal_modulo():
    return render_template('personal.html')

@app.route('/vacunas_reporte')
def vacunas_reporte_modulo():
    return "Esta será la página de reporte de vacunas."

if __name__ == '__main__':
    app.run(debug=True)