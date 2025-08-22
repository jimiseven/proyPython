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
            password="",  # Deja la contraseña vacía por defecto en XAMPP
            database="control_vacunas_v2"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error de conexión a la base de datos: {err}")
        return None

# Ruta de la página de inicio (Panel principal)
@app.route('/')
def index():
    return render_template('index.html')

# Ruta del módulo de Niños
@app.route('/niños')
def niños_modulo():
    db = get_db_connection()
    niños = []
    
    # ------------------ Diagnóstico ------------------
    if db is None:
        print("ERROR: No se pudo conectar a la base de datos.")
    else:
        print("Conexión a la base de datos exitosa.")
        
        cursor = db.cursor(dictionary=True)
        
        # Consulta SQL para obtener la información de los niños y el conteo de vacunas
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
        print(f"La consulta devolvió {len(niños)} registros.")
        # print("Registros:", niños) # Descomentar para ver los datos en la terminal
        
        cursor.close()
        db.close()
    
    return render_template('niños.html', niños=niños)

# Ruta del módulo de Personal Vacunador (aún por desarrollar)
@app.route('/personal')
def personal_modulo():
    return render_template('personal.html')

# Ruta del módulo de Reportes de Vacunas (aún por desarrollar)
@app.route('/vacunas_reporte')
def vacunas_reporte_modulo():
    return "Esta será la página de reporte de vacunas."

if __name__ == '__main__':
    app.run(debug=True)