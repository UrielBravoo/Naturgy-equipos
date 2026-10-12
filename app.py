import os
import pandas as pd
from flask import Flask, render_template, request, jsonify, session

app = Flask(__name__)
app.secret_key = 'clave_secreta_para_sesiones_cat'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max

reporte_activo = {
    'html_tabla': None,
    'total_registros': 0,
    'nombre_archivo': ''
}

USUARIOS = {
    # Operadores por equipo
    'operador_bancau': {'password': 'BanCau2026*', 'rol': 'agente', 'equipo': 'BAN CAU'},
    'operador_noacau': {'password': 'NoaCau2026*', 'rol': 'agente', 'equipo': 'NOA CAU'},
    'operador_sanjuan': {'password': 'SanJuan2026*', 'rol': 'agente', 'equipo': 'ENERGIA SAN JUAN'},
    
    # Líderes (Tienen permisos de carga en cualquier equipo)
    'kparra': {'password': 'admin2026', 'rol': 'lider', 'equipo': 'TODOS'},
    'lherrera': {'password': 'admin2026', 'rol': 'lider', 'equipo': 'TODOS'}
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    usuario = data.get('usuario', '').strip()
    password = data.get('password', '').strip()

    if usuario in USUARIOS and USUARIOS[usuario]['password'] == password:
        session['usuario'] = usuario
        session['rol'] = USUARIOS[usuario]['rol']
        return jsonify({
            'success': True,
            'usuario': usuario,
            'rol': USUARIOS[usuario]['rol']
        })
    
    return jsonify({
        'success': False,
        'message': 'Usuario o contraseña incorrectos.'
    }), 401

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'success': True})

@app.route('/upload', methods=['POST'])
def upload_file():
    global reporte_activo

    if 'file' not in request.files:
        return jsonify({'success': False, 'message': 'No se envió ningún archivo.'}), 400

    file = request.files['file']
    filename = file.filename

    if not filename:
        return jsonify({'success': False, 'message': 'Nombre de archivo no válido.'}), 400

    ext = os.path.splitext(filename)[1].lower()

    try:
        if ext in ['.xls', '.xlsx']:
            df = pd.read_excel(file)
        elif ext == '.csv':
            try:
                df = pd.read_csv(file, encoding='utf-8')
            except UnicodeDecodeError:
                df = pd.read_csv(file, encoding='latin-1', sep=None, engine='python')
        else:
            return jsonify({'success': False, 'message': 'Formato no soportado.'}), 400

        df = df.dropna(how='all')
        tabla_html = df.to_html(classes="tabla-logueos-estilo", index=False, border=0)

        reporte_activo['html_tabla'] = tabla_html
        reporte_activo['total_registros'] = len(df)
        reporte_activo['nombre_archivo'] = filename

        return jsonify({
            'success': True,
            'message': f"Archivo '{filename}' procesado con éxito. Total registros: {len(df)}",
            'total': len(df),
            'html_tabla': tabla_html
        })

    except Exception as e:
        return jsonify({'success': False, 'message': f"Error: {str(e)}"}), 500

@app.route('/obtener_reporte', methods=['GET'])
def obtener_reporte():
    global reporte_activo
    if reporte_activo['html_tabla']:
        return jsonify({
            'success': True,
            'html_tabla': reporte_activo['html_tabla'],
            'total': reporte_activo['total_registros'],
            'archivo': reporte_activo['nombre_archivo']
        })
    
    return jsonify({'success': False, 'message': 'No hay reportes cargados aún.'}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)