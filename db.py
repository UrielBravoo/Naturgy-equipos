import os
import sqlite3

DB_NAME = 'database.db'

def get_db():
    """Establece conexión con SQLite y permite acceso por nombre de columna (tipo JSON/Objeto)."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Crea las tablas e inserta los usuarios desde user.txt si la tabla está vacía."""
    conn = get_db()
    cursor = conn.cursor()

    # Tabla de Usuarios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            rol TEXT NOT NULL,
            equipo TEXT NOT NULL
        )
    ''')

    # Tabla de Reportes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reportes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_archivo TEXT NOT NULL,
            total_registros INTEGER NOT NULL,
            html_tabla TEXT NOT NULL,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()

    # Verificar si la tabla de usuarios está vacía para poblarla desde user.txt
    cursor.execute("SELECT COUNT(*) FROM usuarios")
    total_usuarios = cursor.fetchone()[0]

    txt_path = os.path.join(os.path.dirname(__file__), 'user.txt')

    if total_usuarios == 0 and os.path.exists(txt_path):
        with open(txt_path, 'r', encoding='utf-8') as f:
            for linea in f:
                linea = linea.strip()
                if linea and not linea.startswith('#'):
                    # Espera líneas separadas por coma: username, password, rol, equipo
                    partes = [p.strip() for p in linea.split(',')]
                    if len(partes) == 4:
                        cursor.execute(
                            "INSERT INTO usuarios (username, password, rol, equipo) VALUES (?, ?, ?, ?)",
                            (partes[0], partes[1], partes[2], partes[3])
                        )
        conn.commit()
        print("Usuarios insertados en SQLite3 desde user.txt.")

    conn.close()