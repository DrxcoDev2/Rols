Rols/
│
├── backend/
│   ├── server.py               # Punto de entrada del servidor HTTP
│   ├── routing.py              # Módulo para gestionar rutas y endpoints
│   ├── handlers/               # Funciones que manejan cada ruta
│   ├── middleware.py           # Middleware para peticiones HTTP
│   ├── templates/              # Plantillas HTML para renderizar
│   ├── auth/                   # Módulos para autenticación y autorización
│   ├── db/                    # ORM y conexión con base de datos
│   │    ├── models.py          # Definición de modelos de datos
│   │    ├── orm.py             # Lógica ORM
│   │    └── session.py         # Gestión de sesiones y conexión
│   ├── utils.py                # Funciones utilitarias varias
│   └── config.py               # Configuración general del framework
│
├── frontend/
│   ├── wasm/                   # Código WebAssembly (ej: módulos Rust)
│   ├── static/                 # Archivos estáticos: JS, CSS, imágenes
│   ├── templates/              # Plantillas específicas frontend si aplica
│   └── client.py               # Código para integración WebAssembly y lógica cliente
│
├── tests/                      # Tests unitarios y de integración
│
├── docs/                       # Documentación del framework
│
├── examples/                   # Proyectos de ejemplo usando el framework
│
├── scripts/                    # Scripts útiles (ej: CLI para crear proyectos)
│
├── LICENSE
├── README.md
└── setup.py                    # Configuración para instalación del paquete
