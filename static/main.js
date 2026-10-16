//controllers

document.addEventListener('DOMContentLoaded', () => {
    obtenerReporteGuardado();

    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', login);
    }
});

async function login(e) {
    e.preventDefault();
    const usuario = document.getElementById('usuario').value;
    const password = document.getElementById('password').value;

    try {
        const res = await fetch('/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ usuario, password })
        });

        const data = await res.json();
        if (data.success) {
            document.getElementById('lblUsuario').innerText = data.usuario;
            document.getElementById('lblRol').innerText = data.rol;
            document.getElementById('loginSection').style.display = 'none';
            document.getElementById('appSection').style.display = 'block';
            document.getElementById('userInfo').style.display = 'block';
        } else {
            document.getElementById('loginError').innerText = data.message;
        }
    } catch (err) {
        document.getElementById('loginError').innerText = 'Error al conectar con el servidor.';
    }
}

async function logout() {
    await fetch('/logout', { method: 'POST' });
    location.reload();
}

async function procesarArchivo() {
    const input = document.getElementById('fileInput');
    const status = document.getElementById('uploadStatus');

    if (!input.files[0]) {
        status.innerText = "Por favor selecciona un archivo.";
        return;
    }

    const formData = new FormData();
    formData.append('file', input.files[0]);

    status.innerText = "Procesando...";

    try {
        const res = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        const data = await res.json();
        if (data.success) {
            status.innerText = data.message;
            document.getElementById('tablaContent').innerHTML = data.html_tabla;
        } else {
            status.innerText = "Error: " + data.message;
        }
    } catch (err) {
        status.innerText = "Error al procesar el archivo.";
    }
}

async function obtenerReporteGuardado() {
    try {
        const res = await fetch('/obtener_reporte');
        const data = await res.json();
        if (data.success) {
            document.getElementById('tablaContent').innerHTML = data.html_tabla;
        }
    } catch (err) {
        console.log("No hay reportes previos o el usuario no está logueado.");
    }
}