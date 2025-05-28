# 📚 Personal Library

Un sistema de gestión personal de libros con integración de APIs externas, base de datos PostgreSQL y una interfaz tanto CLI como gráfica (Tkinter). Ideal para usuarios que desean organizar, clasificar y hacer seguimiento de sus lecturas.

## 🚀 Características

- Inserción, búsqueda y categorización de libros.
- Integración con **Google Books API**, **OpenLibrary** y modelos de **HuggingFace** para enriquecer la información.
- Seguimiento de estados de lectura y progreso.
- Interfaz de línea de comandos (`CLI`) y gráfica (`GUI`).
- Base de datos PostgreSQL con seeds, vistas, triggers, funciones y procedimientos almacenados.
- Script automatizado para crear la base de datos desde cero.

## 📦 Requisitos

- Python 3.8+
- PostgreSQL
- API Keys necesarias en archivo `.env`

Instala las dependencias:

```bash
pip install -r requirements.txt
```

## ⚙️ Configuración

Crea un archivo `.env` en la raíz del proyecto:

```env
DB_NAME=library
DB_USER=tu_usuario
DB_PASSWORD=tu_password
DB_HOST=localhost
DB_PORT=5432

HF_API_TOKEN=tu_token_de_huggingface
```

## 🛠️ Inicializar la Base de Datos

Ejecuta el siguiente script para crear la base de datos (si no existe) y poblarla con el esquema, funciones y datos base:

```bash
python app/setup_database.py
```

## 🖥️ Cómo usar

### Interfaz CLI

```bash
python app/ui/cli.py
```

### Interfaz Gráfica (GUI)

```bash
python app/ui/menu.py
```

## 🍎 Ejecutar como una App en Mac (Atajos)

Si eres usuario de macOS, puedes ejecutar la aplicación como si fuera una app gráfica usando la app **Atajos**:

1. Abre la app **Atajos**.
2. Crea un nuevo atajo.
3. Añade la acción **“Ejecutar script de shell”**.
4. Usa el siguiente contenido, ajustando la ruta a donde tengas tu repositorio:

```sh
cd "/tu-ruta/personal-library"
/usr/local/bin/python3 -m app.ui.menu
```

5. Deja el shell en `zsh`, entrada como `Entrada`, y desactiva “Ejecutar como administrador”.
6. Opcional: Añade un ícono y colócalo en el Dock para tener acceso rápido como si fuera una aplicación nativa.

> Asegúrate de que los permisos del sistema permiten ejecutar Python y acceso a Terminal desde Atajos.

## 📁 Estructura del Proyecto

```
personal-library/
│
├── app/
│   ├── database/        ← Scripts SQL y conexión PostgreSQL
│   ├── integration/     ← Integraciones con APIs externas
│   ├── logic/           ← Lógica de negocio (insertar libros, estados)
│   └── ui/              ← CLI y GUI en Tkinter
├── docs/                ← Documentación técnica
├── tests/               ← Scripts de prueba
├── setup_database.py    ← Automatiza la creación de la BD
├── .env                 ← Variables de entorno 
├── requirements.txt     ← Dependencias
└── README.md
```

## 🧪 Pruebas

Próximamente: se integrará `pytest` para pruebas unitarias de módulos clave.

## 🔄 Próximamente

Se implementará una funcionalidad de automatización que permitirá extraer automáticamente datos de archivos digitales (como PDF o EPUB), con el objetivo de registrar libros en la base de datos de forma más rápida y sin intervención manual.

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo [`LICENSE`](LICENSE) para más detalles.

## 🙌 Créditos

Desarrollado por [Eduardo Miramontes](https://github.com/EduardoMiramontes).  
Este proyecto usa recursos públicos de Google Books, OpenLibrary y HuggingFace.

Si reutilizas este proyecto, por favor mantén el aviso de licencia y otórgame crédito como autor original. ¡Gracias!