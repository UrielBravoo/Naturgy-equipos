# 🏢 Naturgy - Sistema de Autenticación y Gestión de Reportes

Sistema web integral desarrollado para **Naturgy / CAT**, enfocado en la gestión operativa, el control de asistencia, el seguimiento de logueos y la centralización de información para los equipos regionales de atención telefónica (**BAN CAU**, **NOA CAU** y **Energía San Juan**).

---

## 🚀 Características principales

- **🔐 Autenticación y control de accesos**
  - **Líderes:** acceso global para la carga de planillas, la gestión de reportes y la administración general.
  - **Operadores:** permisos restringidos exclusivamente a su equipo asignado.

- **💾 Persistencia de datos**
  - Base de datos SQLite3 integrada (`database.db`).
  - Carga automática de usuarios y credenciales iniciales desde el archivo `user.txt`.

- **📊 Módulo de logueos y asistencia consolidada**
  - Procesamiento de planillas descargadas en formatos `.xlsx`, `.xls` y `.csv`.
  - Extracción automática de horarios de **entrada** y **salida** por asesor mediante Pandas.
  - Unificación dinámica de los registros en un tablero diario de asistencia.

- **📢 Información de campaña interactiva**
  - Integración mediante iFrames responsivos con presentaciones oficiales de **Canva**, según el equipo seleccionado.

- **🗂️ Navegación por pestañas corporativas**
  - **👥 Nómina:** listado de personal y distribución por líderes de equipo.
  - **📢 Info Campaña:** presentaciones interactivas de procesos y novedades.
  - **⏱️ Logueos:** control de asistencia y carga de reportes.
  - **📋 Novedades:** registro de incidencias y licencias.
  - **🎯 Calidad:** pautas de atención y evaluaciones.
  - **📈 Métricas:** indicadores clave de rendimiento (KPIs) y selector de mes.

---

## 🛠️ Tecnologías utilizadas

- **Backend:** Python 3, Flask (arquitectura modular con Blueprints), SQLite3, Pandas y OpenPyXL.
- **Frontend:** HTML5, CSS3 (diseño corporativo responsivo) y JavaScript Vanilla (Fetch API).
- **Integraciones:** Canva mediante contenido embebido.
- **Control de versiones:** Git y GitHub (flujo Fork & Pull Request).

---

## 📂 Estructura del proyecto

```text
Naturgy-equipos/
│
├── app.py                  # Punto de entrada principal e inicializador de Flask
├── db.py                   # Conexión a SQLite3 y carga inicial de usuarios
├── database.db             # Base de datos local SQLite3 (se genera automáticamente)
├── user.txt                # Archivo fuente de usuarios y credenciales de prueba
├── uploads/                # Almacenamiento de reportes subidos
│
├── routes/                 # Arquitectura modular con Flask Blueprints
│   ├── auth.py             # Manejo de sesiones, inicio y cierre de sesión
│   └── reportes.py         # Procesamiento y generación de reportes con Pandas
│
├── templates/
│   └── index.html          # Interfaz principal y estructura de pestañas
│
└── static/
    ├── estilos.css         # Hoja de estilos corporativa
    ├── main.js             # Lógica interactiva y peticiones AJAX
    ├── CAT.png             # Isologotipo de CAT
    └── naturgy.png         # Isologotipo de Naturgy
```

---

## 🔑 Credenciales de prueba

| Usuario | Contraseña | Rol | Equipo asignado |
|---|---|---|---|
| `operador_bancau` | `BanCau2026*` | Agente | BAN CAU |
| `operador_noacau` | `NoaCau2026*` | Agente | NOA CAU |
| `operador_sanjuan` | `SanJuan2026*` | Agente | ENERGÍA SAN JUAN |
| `kparra` | `admin2026` | Líder | TODOS |
| `lherrera` | `admin2026` | Líder | TODOS |

> **⚠️ Importante:** estas credenciales son únicamente para pruebas. No utilices contraseñas reales ni publiques credenciales sensibles en un repositorio público.

---

## ⚙️ Guía de instalación y ejecución local

### Paso 1: Instalar las dependencias

Abre la terminal de VS Code en la carpeta raíz del proyecto e instala los paquetes necesarios, uno por uno.

**1. Instalar Flask**

```bash
py -m pip install flask
```

**2. Instalar Pandas**

```bash
py -m pip install pandas
```

**3. Instalar OpenPyXL**

```bash
py -m pip install openpyxl
```

### Paso 2: Verificar los archivos necesarios

Antes de iniciar el servidor, verifica que el archivo `user.txt` se encuentre en la raíz del proyecto y que la estructura de carpetas sea correcta.

### Paso 3: Ejecutar el servidor web

Desde la terminal de VS Code, ejecuta:

```bash
py app.py
```

### Paso 4: Abrir la aplicación en el navegador

Una vez iniciado el servidor, ingresa a la siguiente dirección:

[http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 📝 Notas

- La base de datos SQLite3 se almacena localmente en `database.db`.
- Los reportes cargados se almacenan en la carpeta `uploads/`.
- Las dependencias deben instalarse en el entorno de Python utilizado para ejecutar la aplicación.
- El funcionamiento de la carga inicial de usuarios depende de la implementación existente en el proyecto.
