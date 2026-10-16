from flask import Blueprint, request, jsonify, session
from db import get_db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    usuario_input = data.get('usuario', '').strip()
    password_input = data.get('password', '').strip()

    conn = get_db()
    cursor = conn.cursor()
    
    # Consulta SQL directa parametrizada
    cursor.execute(
        "SELECT * FROM usuarios WHERE username = ? AND password = ?",
        (usuario_input, password_input)
    )
    user = cursor.fetchone()
    conn.close()

    if user:
        session['usuario'] = user['username']
        session['rol'] = user['rol']
        return jsonify({
            'success': True,
            'usuario': user['username'],
            'rol': user['rol']
        })

    return jsonify({
        'success': False,
        'message': 'Usuario o contraseña incorrectos.'
    }), 401

@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'success': True})