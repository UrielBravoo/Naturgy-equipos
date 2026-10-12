let equipoSeleccionado = "";
let rolUsuario = "";

function abrirLogin(nombreEquipo) {
    equipoSeleccionado = nombreEquipo;
    const modalTitle = document.getElementById("modalTitle");
    const loginModal = document.getElementById("loginModal");
    
    if (modalTitle) modalTitle.innerHTML = '<i class="fa-solid fa-shield-halved"></i> Acceso a ' + nombreEquipo;
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

            rolUsuario = data.rol.toLowerCase();

            document.getElementById("equipo-section").style.display = "none";
            document.getElementById("dashboard-section").style.display = "block";

            document.getElementById("user-display").innerText = data.usuario;
            document.getElementById("role-display").innerText = data.rol.toUpperCase();

            configurarVistasEquipo(equipoSeleccionado);

            // Control de paneles de líder
            document.querySelectorAll('.leader-panel').forEach(panel => {
                panel.style.display = (rolUsuario === "lider") ? "block" : "none";
            });

            // Cargar datos iniciales
            cargarReporte('novedades');
            cargarReporte('logueos');
            cargarReporte('calidad');
            cargarReporte('tmo');
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
    const btnNomina = document.getElementById("tab-btn-nomina");

    document.querySelectorAll('.team-ppt').forEach(ppt => ppt.style.display = 'none');

    if (equipo.includes("BAN")) {
        if (labelEquipo) labelEquipo.innerText = "Ban";
        if (headerTitle) headerTitle.innerHTML = '<i class="fa-solid fa-circle-info"></i> Información del Ban / Novedades';
        document.getElementById("ppt-bancau").style.display = "block";
        if (btnNomina) btnNomina.style.display = "inline-block";
    } else if (equipo.includes("SAN JUAN")) {
        if (labelEquipo) labelEquipo.innerText = "San Juan";
        if (headerTitle) headerTitle.innerHTML = '<i class="fa-solid fa-circle-info"></i> Información de Energía San Juan';
        document.getElementById("ppt-sanjuan").style.display = "block";
        if (btnNomina) btnNomina.style.display = "none";
    } else if (equipo.includes("NOA")) {
        if (labelEquipo) labelEquipo.innerText = "NOA";
        if (headerTitle) headerTitle.innerHTML = '<i class="fa-solid fa-circle-info"></i> Información de NOA CAU';
        document.getElementById("ppt-noacau").style.display = "block";
        if (btnNomina) btnNomina.style.display = "none";
    }

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

// Control genérico de subpestañas (Calidad y TMO)
function showSubTab(modulo, subTabName) {
    const parentTab = document.getElementById('tab-' + modulo);
    if (!parentTab) return;

    parentTab.querySelectorAll('.subtab-content').forEach(subTab => subTab.style.display = 'none');
    parentTab.querySelectorAll('.subnav-tab').forEach(btn => btn.classList.remove('active'));

    const targetSubTab = document.getElementById(`subtab-${modulo}-${subTabName}`) || document.getElementById(`subtab-${subTabName}`);
    const targetSubBtn = document.getElementById(`subtab-btn-${subTabName}`) || document.getElementById(`subtab-btn-${modulo}-${subTabName}`);

    if (targetSubTab) targetSubTab.style.display = 'block';
    if (targetSubBtn) targetSubBtn.classList.add('active');
}

function cambiarPeriodoNovedades(periodo) {
    cargarReporte('novedades', periodo);
}

function cambiarMes(tipoReporte, mes) {
    cargarReporte(tipoReporte, mes);
}

function cargarReporte(tipoReporte, parametroFecha = null) {
    let selectElem;
    if (tipoReporte === 'novedades') {
        selectElem = document.getElementById('select-periodo-novedades');
    } else {
        selectElem = document.getElementById(`select-mes-${tipoReporte}`);
    }

    const valorFecha = parametroFecha || (selectElem ? selectElem.value : "2026-10");

    fetch(`/obtener_reporte?tipo=${tipoReporte}&fecha=${valorFecha}&equipo=${encodeURIComponent(equipoSeleccionado)}`)
    .then(response => response.json())
    .then(data => {
        // Cargar en los contenedores correspondientes
        const containerGeneral = document.getElementById(`table-container-${tipoReporte}`);
        if (containerGeneral && data.html_tabla) {
            containerGeneral.innerHTML = data.html_tabla;
        }
    })
    .catch(() => {
        console.log(`Panel de ${tipoReporte} listo.`);
    });
}

function subirArchivo(tipoReporte) {
    const inputIdMap = {
        'novedades': 'excelFileNovedades',
        'logueos': 'excelFileLogueos',
        'calidad': 'excelFileCalidad',
        'tmo': 'excelFileTmo'
    };

    const fileInput = document.getElementById(inputIdMap[tipoReporte]);
    let selectElem = (tipoReporte === 'novedades') 
        ? document.getElementById('select-periodo-novedades') 
        : document.getElementById(`select-mes-${tipoReporte}`);

    const valorFecha = selectElem ? selectElem.value : "";

    if (!fileInput || fileInput.files.length === 0) {
        alert("⚠️ Selecciona un archivo (.xlsx, .xls o .csv) antes de subir.");
        return;
    }

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);
    formData.append("tipo", tipoReporte);
    formData.append("fecha", valorFecha);
    formData.append("equipo", equipoSeleccionado);

    fetch("/upload", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("✅ " + data.message);
            fileInput.value = "";
            cargarReporte(tipoReporte, valorFecha);
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