import os
import pandas as pd
from flask import Blueprint, request, jsonify
from db import get_db

reportes_bp = Blueprint('reportes', __name__)

@reportes_bp.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'success': False, 'message': 'No se envió ningún archivo.'}), 400

    file = request.files['file']
    filename = file.filename

    if not filename:
        return jsonify({'success': False, 'message': 'Nombre de archivo no válido.'}), 400

    ext = os.path.splitext(filename)[1].lower()

    try:
        if ext in ['.xls', '.xlsx']:
            # Lee automáticamente la solapa 'OCTUBRE' si existe, o la primera por defecto
            try:
                df = pd.read_excel(file, sheet_name='OCTUBRE')
            except Exception:
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

        # Guardar persistencia directa en SQLite
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO reportes (nombre_archivo, total_registros, html_tabla) VALUES (?, ?, ?)",
            (filename, len(df), tabla_html)
        )
        conn.commit()
        conn.close()

        return jsonify({
            'success': True,
            'message': f"Archivo '{filename}' procesado y guardado en SQLite con éxito. Total registros: {len(df)}",
            'total': len(df),
            'html_tabla': tabla_html
        })

    except Exception as e:
        return jsonify({'success': False, 'message': f"Error: {str(e)}"}), 500

@reportes_bp.route('/obtener_reporte', methods=['GET'])
def obtener_reporte():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM reportes ORDER BY id DESC LIMIT 1")
    ultimo = cursor.fetchone()
    conn.close()

    if ultimo:
        return jsonify({
            'success': True,
            'html_tabla': ultimo['html_tabla'],
            'total': ultimo['total_registros'],
            'archivo': ultimo['nombre_archivo']
        })

    return jsonify({'success': False, 'message': 'No hay reportes cargados aún.'}), 404