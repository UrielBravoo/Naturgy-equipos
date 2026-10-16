from flask import Flask, render_template
from db import init_db
from routes.auth import auth_bp
from routes.reportes import reportes_bp

app = Flask(__name__)
app.secret_key = 'clave_secreta_para_sesiones_cat'

# Corregido: Limite de subida de 16 MB
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Registrar los Blueprints (módulos de rutas)
app.register_blueprint(auth_bp)
app.register_blueprint(reportes_bp)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    # Inicializa la base de datos SQLite y carga user.txt al arrancar
    init_db()
    app.run(debug=True, port=5000)