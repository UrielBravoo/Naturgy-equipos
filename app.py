import os
import pandas as pd
from flask import Flask, render_template, request, jsonify, session, send_from_directory
from dotenv import load_dotenv
from scripts.procesar_excel import procesar_logueos_orion

load_dotenv()

app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = os.getenv('SECRET_KEY', 'clave_secreta_naturgy_2026')

# Configuración de base de usuarios leyendo desde .env
def obtener_usuarios():
    return {
        os.getenv('USUARIO_EQUIPO_BAN_CAU'): {"pass": os.getenv('PASS_EQUIPO_BAN_CAU'), "rol": "operador", "equipo": "NATURGY BAN CAU"},
        os.getenv('USUARIO_EQUIPO_NOA_CAU'): {"pass": os.getenv('PASS_EQUIPO_NOA_CAU'), "rol": "operador", "equipo": "NATURGY NOA CAU"},
        os.getenv('USUARIO_EQUIPO_SAN_JUAN'): {"pass": os.getenv('PASS_EQUIPO_SAN_JUAN'), "rol": "operador", "equipo": "NATURGY ENERGIA SAN JUAN"},
        os.getenv('USUARIO_LIDER_1'): {"pass": os.getenv('PASS_LIDER_1'), "rol": "lider", "equipo": "TODOS"},
        os.getenv('USUARIO_LIDER_2'): {"pass": os.getenv('PASS_LIDER_2'), "rol": "lider", "equipo": "TODOS"}
    }

@app.route('/')
def index():
    return render_template('index.html')

# Servir archivos estáticos de la carpeta assets (Logos)
@app.route('/assets/<path:filename>')
def serve_assets(filename):
    return send_from_directory('assets', filename)

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    usuario = data.get('usuario')
    password = data.get('password')
    equipo = data.get('equipo')

    users_db = obtener_usuarios()
    user_info = users_db.get(usuario)

    if user_info and user_info['pass'] == password:
        # Si es operador, validar que pertenezca al equipo seleccionado o sea líder
        if user_info['rol'] == 'operador' and user_info['equipo'] != equipo:
            return jsonify({"status": "error", "mensaje": f"El usuario no tiene permiso para el equipo {equipo}"}), 403

        session['usuario'] = usuario
        session['rol'] = user_info['rol']
        session['equipo'] = equipo if user_info['rol'] == 'operador' else 'TODOS'

        return jsonify({
            "status": "success",
            "rol": user_info['rol'],
            "equipo": session['equipo'],
            "usuario": usuario
        })

    return jsonify({"status": "error", "mensaje": "Usuario o contraseña incorrectos"}), 401

@app.route('/get-data', methods=['GET'])
def get_data():
    if 'usuario' not in session:
        return jsonify({"error": "No autorizado"}), 401

    # Busca primero el archivo subido o usa el CSV original de logueos
    ruta_csv = 'uploads/ultimo_reporte.xlsx'
    if not os.path.exists(ruta_csv):
        ruta_csv = 'Logueos Naturgy BAN CAU SEPT-OCT(Log Oct).csv'

    resultado = procesar_logueos_orion(ruta_csv)
    return jsonify(resultado)

@app.route('/upload-excel', methods=['POST'])
def upload_excel():
    # Permiso exclusivo para Líderes
    if session.get('rol') != 'lider':
        return jsonify({"error": "Acceso denegado. Permiso exclusivo para Líderes."}), 403

    if 'file' not in request.files:
        return jsonify({"error": "No se subió ningún archivo"}), 400

    file = request.files['file']
    os.makedirs('uploads', exist_ok=True)
    filepath = os.path.join('uploads', 'ultimo_reporte.xlsx')
    file.save(filepath)

    resultado = procesar_logueos_orion(filepath)
    return jsonify({"status": "success", "mensaje": "Archivo cargado y procesado exitosamente", "detalles": resultado})

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)