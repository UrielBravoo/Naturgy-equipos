let equipoSeleccionado = "";

function abrirLogin(nombreEquipo) {
    equipoSeleccionado = nombreEquipo;
    const modalTitle = document.getElementById("modalTitle");
    const loginModal = document.getElementById("loginModal");
    
    if (modalTitle) modalTitle.innerText = "Acceso a " + nombreEquipo;
    if (loginModal) loginModal.style.display = "block";
    
    setTimeout(() => {
        const userInput = document.getElementById("usuario");
        if (userInput) userInput.focus();
    }, 100);
}

function cerrarLogin() {
    const loginModal = document.getElementById("loginModal");
    if (loginModal) loginModal.style.display = "none";
    document.getElementById("usuario").value = "";
    document.getElementById("password").value = "";
}

function validarAcceso(event) {
    event.preventDefault();

    const usuarioInput = document.getElementById("usuario").value.trim();
    const passwordInput = document.getElementById("password").value.trim();

    if (!usuarioInput || !passwordInput) {
        alert("Por favor completa el usuario y la contraseña.");
        return;
    }

    fetch("/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            usuario: usuarioInput,
            password: passwordInput,
            equipo: equipoSeleccionado
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            cerrarLogin();

            document.getElementById("equipo-section").style.display = "none";
            document.getElementById("dashboard-section").style.display = "block";

            document.getElementById("user-display").innerText = data.usuario;
            document.getElementById("role-display").innerText = data.rol.toUpperCase();

            // Configurar vistas e información del equipo correspondiente
            configurarVistasEquipo(equipoSeleccionado);

            // CONTROL DE ROL: Solo si ingresa un Líder se activa la caja de subir archivos
            const leaderPanel = document.getElementById("leader-panel");
            if (leaderPanel) {
                if (data.rol.toLowerCase() === "lider") {
                    leaderPanel.style.display = "block";
                } else {
                    leaderPanel.style.display = "none";
                }
            }

            cargarReporte();
        } else {
            alert("❌ Error: " + data.message);
        }
    })
    .catch(error => {
        console.error("Error en la autenticación:", error);
        alert("❌ Error de comunicación al autenticar.");
    });
}

function configurarVistasEquipo(equipo) {
    const labelEquipo = document.getElementById("team-info-label");
    const headerTitle = document.getElementById("info-title-header");

    // Ocultar todas las presentaciones activas
    document.querySelectorAll('.team-ppt').forEach(ppt => ppt.style.display = 'none');

    // Cambiar texto de pestaña e iframe correspondiente
    if (equipo.includes("BAN")) {
        if (labelEquipo) labelEquipo.innerText = "Ban";
        if (headerTitle) headerTitle.innerText = "Información del Ban / Novedades";
        const pptBan = document.getElementById("ppt-bancau");
        if (pptBan) pptBan.style.display = "block";
    } else if (equipo.includes("SAN JUAN")) {
        if (labelEquipo) labelEquipo.innerText = "San Juan";
        if (headerTitle) headerTitle.innerText = "Información de Energía San Juan";
        const pptSJ = document.getElementById("ppt-sanjuan");
        if (pptSJ) pptSJ.style.display = "block";
    } else if (equipo.includes("NOA")) {
        if (labelEquipo) labelEquipo.innerText = "NOA";
        if (headerTitle) headerTitle.innerText = "Información de NOA CAU";
        const pptNoa = document.getElementById("ppt-noacau");
        if (pptNoa) pptNoa.style.display = "block";
    }

    // Abrir siempre la primera pestaña (Info) por defecto
    showTab('info');
}

function showTab(tabName) {
    document.querySelectorAll('.tab-content').forEach(tab => tab.style.display = 'none');
    document.querySelectorAll('.nav-tab').forEach(btn => btn.classList.remove('active'));

    const targetTab = document.getElementById('tab-' + tabName);
    const targetBtn = document.getElementById('tab-btn-' + tabName);

    if (targetTab) targetTab.style.display = 'block';
    if (targetBtn) targetBtn.classList.add('active');
}

function cargarReporte() {
    const tableContainer = document.getElementById("table-container");
    if (!tableContainer) return;

    tableContainer.innerHTML = "<p>Cargando información del equipo...</p>";

    fetch("/obtener_reporte")
    .then(response => response.json())
    .then(data => {
        if (data.success && data.html_tabla) {
            tableContainer.innerHTML = data.html_tabla;
        } else {
            tableContainer.innerHTML = "<p>No hay reportes cargados para este equipo aún.</p>";
        }
    })
    .catch(() => {
        tableContainer.innerHTML = "<p>Panel de reporte listo. Esperando carga de archivo por el Líder.</p>";
    });
}

function subirArchivo() {
    const fileInput = document.getElementById("excelFile");

    if (!fileInput || fileInput.files.length === 0) {
        alert("⚠️ Selecciona un archivo (.xlsx, .xls o .csv) antes de subir.");
        return;
    }

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    fetch("/upload", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("✅ " + data.message);
            fileInput.value = "";
            cargarReporte();
        } else {
            alert("❌ Error: " + data.message);
        }
    })
    .catch(error => {
        console.error("Error al subir archivo:", error);
        alert("❌ Error de comunicación al subir el archivo.");
    });
}

function cerrarSesion() {
    fetch("/logout", { method: "POST" })
    .then(() => {
        document.getElementById("dashboard-section").style.display = "none";
        document.getElementById("equipo-section").style.display = "flex";
    })
    .catch(() => {
        document.getElementById("dashboard-section").style.display = "none";
        document.getElementById("equipo-section").style.display = "flex";
    });
}