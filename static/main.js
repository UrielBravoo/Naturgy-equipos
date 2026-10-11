let equipoSeleccionado = "";

function abrirLogin(nombreEquipo) {
    equipoSeleccionado = nombreEquipo;
    document.getElementById("modalTitle").innerText = nombreEquipo === 'LIDER' ? 'Acceso Líderes' : 'Acceso ' + nombreEquipo;
    document.getElementById("loginModal").style.display = "block";
}

function cerrarLogin() {
    document.getElementById("loginModal").style.display = "none";
    document.getElementById("usuario").value = "";
    document.getElementById("password").value = "";
}

async function validarAcceso(event) {
    event.preventDefault();
    const usuario = document.getElementById("usuario").value;
    const pass = document.getElementById("password").value;

    try {
        const response = await fetch('/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ usuario, password: pass, equipo: equipoSeleccionado })
        });

        const data = await response.json();

        if (response.ok && data.status === "success") {
            cerrarLogin();
            mostrarDashboard(data.usuario, data.rol, data.equipo);
            cargarTablaDatos();
        } else {
            alert(data.mensaje || "Credenciales inválidas");
        }
    } catch (err) {
        alert("Error de conexión al servidor.");
    }
}

function mostrarDashboard(usuario, rol, equipo) {
    document.getElementById("equipo-section").style.display = "none";
    document.getElementById("dashboard-section").style.display = "block";

    document.getElementById("user-display").innerText = usuario;
    document.getElementById("role-display").innerText = rol === 'lider' ? 'Líder (Edición/Carga)' : `Operador (${equipo})`;

    // Control de acceso: Ocultar panel de carga para operadores
    if (rol === 'lider') {
        document.getElementById("leader-panel").style.display = "block";
    } else {
        document.getElementById("leader-panel").style.display = "none";
    }
}

async function cargarTablaDatos() {
    const container = document.getElementById("table-container");
    container.innerHTML = "<p>Cargando registros...</p>";

    try {
        const res = await fetch('/get-data');
        const data = await res.json();

        if (data.status === "ok" && data.datos.length > 0) {
            let html = "<table><thead><tr>";
            data.columnas.forEach(col => {
                html += `<th>${col}</th>`;
            });
            html += "</tr></thead><tbody>";

            data.datos.forEach(row => {
                html += "<tr>";
                data.columnas.forEach(col => {
                    html += `<td>${row[col] || ''}</td>`;
                });
                html += "</tr>";
            });

            html += "</tbody></table>";
            container.innerHTML = html;
        } else {
            container.innerHTML = "<p>No hay registros disponibles para mostrar.</p>";
        }
    } catch (e) {
        container.innerHTML = "<p>Error al cargar el reporte.</p>";
    }
}

async function subirArchivo() {
    const fileInput = document.getElementById("excelFile");
    if (!fileInput.files || fileInput.files.length === 0) {
        alert("Por favor selecciona un archivo Excel o CSV.");
        return;
    }

    const formData = new FormData();
    formData.append("file", fileInput.files);

    try {
        const response = await fetch('/upload-excel', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();
        if (response.ok) {
            alert("¡Archivo subido y procesado correctamente!");
            cargarTablaDatos();
        } else {
            alert(result.error || "Error al subir el archivo.");
        }
    } catch (err) {
        alert("Error en la solicitud de carga.");
    }
}

function cerrarSesion() {
    fetch('/logout', { method: 'POST' }).then(() => {
        document.getElementById("dashboard-section").style.display = "none";
        document.getElementById("equipo-section").style.display = "flex";
    });
}