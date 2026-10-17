import os
import pandas as pd
import re
from flask import Flask, render_template, request, jsonify, session
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'clave_secreta_naturgy_2026'

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Base de datos de usuarios (USERS.txt)
USUARIOS = {
    "kparra": {"password": "admin2026", "rol": "lider", "equipo": "TODOS"},
    "lherrera": {"password": "admin2026", "rol": "lider", "equipo": "TODOS"},
    "operador_bancau": {"password": "BanCau2026*", "rol": "operador", "equipo": "NATURGY BAN CAU"},
    "operador_noacau": {"password": "NoaCau2026*", "rol": "operador", "equipo": "NATURGY NOA CAU"},
    "operador_sanjuan": {"password": "SanJuan2026*", "rol": "operador", "equipo": "NATURGY ENERGIA SAN JUAN"}
}

def clean_str(val):
    if pd.isna(val) or val is None:
        return ''
    return str(val).strip()

def procesar_archivo_reporte(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    df_raw = None
    
    # 1. Intentar lectura como Excel
    if ext in ['.xlsx', '.xls']:
        for engine in ['openpyxl', 'xlrd', None]:
            try:
                df_raw = pd.read_excel(filepath, sheet_name=0, header=None, engine=engine)
                if df_raw is not None and not df_raw.empty:
                    break
            except Exception:
                pass

    # 2. Intentar lectura como CSV
    if df_raw is None or df_raw.empty:
        for enc in ['utf-8', 'latin1', 'cp1252']:
            for sep in [';', ',', '\t', None]:
                try:
                    df_raw = pd.read_csv(filepath, sep=sep, encoding=enc, header=None, on_bad_lines='skip', engine='python')
                    if df_raw is not None and not df_raw.empty and df_raw.shape[1] > 1:
                        break
                except Exception:
                    pass
            if df_raw is not None and not df_raw.empty and df_raw.shape[1] > 1:
                break

    if df_raw is None or df_raw.empty:
        return []

    raw_text_list = [clean_str(x) for x in df_raw.values.flatten()]
    raw_text = ' '.join([x for x in raw_text_list if x])

    # CASO A: Reporte Individual del sistema (reporte_csv.csv)
    if 'AGENTE:' in raw_text.upper() or 'REPORTE MENSUAL POR AGENTE' in raw_text.upper():
        agente = 'ASESOR'
        for r_idx in range(min(10, len(df_raw))):
            row_vals = [clean_str(x) for x in df_raw.iloc[r_idx].values]
            row_str = ' '.join([x for x in row_vals if x])
            if 'AGENTE:' in row_str.upper():
                m = re.search(r'AGENTE:\s*([^;|\n\r]+)', row_str, re.IGNORECASE)
                if m:
                    agente = m.group(1).strip()
                    break

        header_idx = None
        for r_idx in range(min(15, len(df_raw))):
            row_vals = [clean_str(x) for x in df_raw.iloc[r_idx].values]
            row_str = ' '.join([x for x in row_vals if x]).upper()
            if 'DESCRIPCION' in row_str or 'DESCRIPCIÓN' in row_str:
                header_idx = r_idx
                break

        if header_idx is not None:
            header_row = [clean_str(x) for x in df_raw.iloc[header_idx].values]
            df_data = df_raw.iloc[header_idx + 1:].copy()
            df_data.columns = header_row
        else:
            df_data = df_raw.copy()

        desc_col = None
        for col in df_data.columns:
            if 'DESCRIP' in str(col).upper():
                desc_col = col
                break

        if desc_col is None:
            return []

        df_in = df_data[df_data[desc_col].astype(str).str.strip().str.upper() == 'HORA DE ENTRADA']
        df_out = df_data[df_data[desc_col].astype(str).str.strip().str.upper() == 'HORA DE SALIDA']

        if df_in.empty or df_out.empty:
            return []

        ignore_keywords = ['GRUPO', 'DESCRIP', 'TOTAL', 'UNNAMED', 'NAN', 'NONE']
        date_cols = []
        for col in df_data.columns:
            c_str = str(col).strip()
            c_upper = c_str.upper()
            if c_str != '' and not any(k in c_upper for k in ignore_keywords):
                date_cols.append(col)

        row1 = {'Asesor': agente, 'DESCRIPCION': 'Hora de Entrada'}
        row2 = {'Asesor': '', 'DESCRIPCION': 'Hora de Salida'}

        for col in date_cols:
            col_name = str(col).strip()
            v_in_vals = df_in[col].values
            v_out_vals = df_out[col].values
            
            v_in = v_in_vals[0] if len(v_in_vals) > 0 else '---'
            v_out = v_out_vals[0] if len(v_out_vals) > 0 else '---'
            
            str_in = clean_str(v_in)
            str_out = clean_str(v_out)
            
            row1[col_name] = str_in if str_in and str_in.lower() != 'nan' else '---'
            row2[col_name] = str_out if str_out and str_out.lower() != 'nan' else '---'

        return [pd.DataFrame([row1, row2])]

    # CASO B: Archivo grupal (logueos.jpg)
    blocks = []
    current_agent = None
    dates = []

    for r_idx in range(len(df_raw)):
        row_vals = [clean_str(x) for x in df_raw.iloc[r_idx].values]
        row_str = ' '.join([x for x in row_vals if x]).upper()
        
        v0 = row_vals[0] if len(row_vals) > 0 else ''
        v1 = row_vals[1] if len(row_vals) > 1 else ''

        if v1.upper() in ['DESCRIPCION', 'DESCRIPCIÓN']:
            current_agent = v0 if v0 else 'ASESOR'
            if r_idx + 1 < len(df_raw):
                next_vals = [clean_str(x) for x in df_raw.iloc[r_idx + 1].values]
                dates = [v for v in next_vals if v and any(t in v.lower() for t in ['oct', 'sep', '/', '-'])]
            continue

        if 'HORA DE ENTRADA' in row_str:
            in_vals = [v for v in row_vals if v]
            out_vals = []
            if r_idx + 1 < len(df_raw):
                out_vals = [clean_str(x) for x in df_raw.iloc[r_idx + 1].values if clean_str(x)]

            row1 = {'Asesor': current_agent or 'ASESOR', 'DESCRIPCION': 'Hora de Entrada'}
            row2 = {'Asesor': '', 'DESCRIPCION': 'Hora de Salida'}

            in_times = [v for v in in_vals if v not in [current_agent, 'DESCRIPCION', 'Hora de Entrada'] and v.lower() != 'nan']
            out_times = [v for v in out_vals if v not in ['DESCRIPCION', 'Hora de Salida'] and v.lower() != 'nan']

            for d_idx, d_name in enumerate(dates):
                v_in = in_times[d_idx] if d_idx < len(in_times) else '---'
                v_out = out_times[d_idx] if d_idx < len(out_times) else '---'
                row1[d_name] = v_in if v_in and v_in.lower() != 'nan' else '---'
                row2[d_name] = v_out if v_out and v_out.lower() != 'nan' else '---'

            blocks.append(pd.DataFrame([row1, row2]))

    return blocks

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    usuario = data.get('usuario', '').strip()
    password = data.get('password', '').strip()
    equipo_solicitado = data.get('equipo', '').strip()

    if usuario not in USUARIOS or USUARIOS[usuario]['password'] != password:
        return jsonify({"success": False, "message": "Usuario o contraseña incorrectos"}), 401

    user_info = USUARIOS[usuario]

    if user_info['rol'] != 'lider' and user_info['equipo'] != equipo_solicitado:
        return jsonify({
            "success": False, 
            "message": f"Acceso denegado: El usuario '{usuario}' solo puede ingresar al equipo '{user_info['equipo']}'."
        }), 403

    session['usuario'] = usuario
    session['rol'] = user_info['rol']
    session['equipo'] = equipo_solicitado if user_info['rol'] == 'lider' else user_info['equipo']

    return jsonify({
        "success": True,
        "usuario": usuario,
        "rol": user_info['rol'],
        "equipo": session['equipo']
    })

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({"success": True})

@app.route('/upload', methods=['POST'])
def upload_file():
    if session.get('rol') != 'lider':
        return jsonify({"success": False, "message": "Se requieren permisos de Líder."}), 403

    if 'file' not in request.files:
        return jsonify({"success": False, "message": "No se adjuntó ningún archivo."}), 400

    file = request.files['file']
    if file.filename == '' or file.filename == '[object FileList]':
        return jsonify({"success": False, "message": "Por favor selecciona un archivo válido."}), 400

    filename = secure_filename(file.filename)
    ext = os.path.splitext(filename)[1].lower()
    
    if ext not in ['.csv', '.xlsx', '.xls']:
        return jsonify({"success": False, "message": "Formato de archivo no permitido. Debe ser .csv, .xlsx o .xls."}), 400

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    return jsonify({
        "success": True,
        "message": f"Reporte '{filename}' cargado correctamente."
    })

@app.route('/obtener_reporte', methods=['GET'])
def obtener_reporte():
    if 'usuario' not in session:
        return jsonify({"success": False, "message": "Sesión no iniciada"}), 401

    equipo_activo = session.get('equipo')

    archivos = [
        os.path.join(app.config['UPLOAD_FOLDER'], f) 
        for f in os.listdir(app.config['UPLOAD_FOLDER']) 
        if f.endswith(('.csv', '.xlsx', '.xls'))
    ]

    if not archivos:
        return jsonify({
            "success": False, 
            "message": "No hay reportes cargados aún para este equipo."
        })

    try:
        all_blocks = []
        for archivo in archivos:
            blocks = procesar_archivo_reporte(archivo)
            all_blocks.extend(blocks)

        if not all_blocks:
            return jsonify({"success": False, "message": "No se pudieron procesar los datos de las planillas."})

        # Desduplicar asesores manteniendo la última versión subida
        seen_advisors = set()
        dedup_blocks = []
        for block in reversed(all_blocks):
            adv_name = clean_str(block['Asesor'].iloc[0]) if len(block) > 0 and 'Asesor' in block.columns else ''
            if adv_name and adv_name != 'ASESOR':
                if adv_name not in seen_advisors:
                    seen_advisors.add(adv_name)
                    dedup_blocks.append(block)
            else:
                dedup_blocks.append(block)

        dedup_blocks.reverse()
        df_consolidado = pd.concat(dedup_blocks, ignore_index=True).fillna('---')

        html_tabla = df_consolidado.to_html(
            classes='table table-striped tabla-reporte', 
            index=False
        )

        return jsonify({
            "success": True,
            "equipo": equipo_activo,
            "html_tabla": html_tabla
        })

    except Exception as e:
        return jsonify({
            "success": False, 
            "message": f"Error al procesar la consolidación: {str(e)}"
        }), 500

if __name__ == '__main__':
    print("\n🚀 Servidor activo en http://127.0.0.1:5000\n")
    app.run(debug=True, host='127.0.0.1', port=5000)