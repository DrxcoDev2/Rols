# 🐍 Rols — Framework Web Fullstack en Python

**Rols** es un micro-framework web creado en Python puro, diseñado para manejar tanto el backend como el frontend utilizando una arquitectura sencilla, rápida y extensible. Está inspirado en frameworks como Flask y Next.js, pero con plantillas renderizadas directamente desde el servidor y sesiones incorporadas.

---
![Static Badge](https://img.shields.io/github/stars/drxcodev2/rols)
![Static Gadge MIT](https://img.shields.io/badge/licencia-MIT-orange?style=flat)
![Static Gadge Python](https://img.shields.io/badge/python-3.9-blue?style=flat)
![Version](https://img.shields.io/badge/version-1.0.5-green?style=flat)

## 🚀 Características

- 🧭 Routing con decoradores (`@server.route`)
- 📄 Motor de plantillas HTML simple (`{{ variables }}`, `{% bloques %}`)
- 🔒 Gestión de sesiones mediante cookies (`session['usuario']`)
- 🧠 Soporte para métodos `GET` y `POST`
- 📦 Sin dependencias externas
- 🪄 API fácil de usar y entender
- 🧩 Separación clara entre rutas, lógica y vistas

---

## 📦 Instalación

```bash
git clone https://github.com/tu_usuario/rols
cd rols
python backend/server.py
```
# 🧪 Estructura de proyecto
```
Rols/
├── backend/
│   ├── server.py          # Servidor HTTP personalizado
│   └── handlers.py        # Funciones asociadas a rutas
├── templates/
│   ├── index.html         # Plantillas HTML renderizadas en servidor
│   └── login_response.html
├── static/                # Archivos estáticos (futuro)
└── README.md              # Este archivo
```

# 👨‍💻 Uso básico
```python
from rols import HTTPServer, SimpleTemplate

server = HTTPServer()

@server.route("/", method="GET")
async def home(body=None, session=None, **kwargs):
    tpl = SimpleTemplate("templates/index.html")
    return tpl.render({'name': session.get('user', 'Invitado')})

@server.route("/login", method="POST")
async def login(body=None, session=None, **kwargs):
    if body.get("username") == "admin":
        session["user"] = "admin"
        return "Login exitoso"
    return "Credenciales incorrectas"

if __name__ == "__main__":
    import asyncio
    asyncio.run(server.run())
```
## Consejos 
```python
"""
use client
use @backend 
"""
# para aclarar que todo esta conectado al backend 
# mejora la velocidad y produce menos errores
```
## Manejo de archivos estaticos
**No hace falta vincular a una plantilla .html**
```python
from backend.server import HTTPServer
import asyncio

server = HTTPServer(static_dir='static')

# Ruta normal
@server.route('/')
async def index():
    return '''
    <html>
        <head>
            <link rel="stylesheet" href="/static/css/style.css">
        </head>
        <body>
            <h1>Welcome!</h1>
            <img src="/static/images/logo.png">
            <script src="/static/js/main.js"></script>
        </body>
    </html>
    '''


import os

os.makedirs('static/css', exist_ok=True)
with open('static/css/style.css', 'w') as f:
    f.write('''
    body {
        font-family: Arial, sans-serif;
        margin: 40px;
    }
    ''')


os.makedirs('static/js', exist_ok=True)
with open('static/js/main.js', 'w') as f:
    f.write('''
    console.log('Static file system working!');
    ''')

if __name__ == '__main__':
    asyncio.run(server.run())
```

# 🧠 Plantillas personalizadas
```html
<h1>Hola {{ name }}</h1>
{% if name == 'admin' %}
<p>Tienes acceso completo.</p>
{% else %}
<p>Acceso limitado.</p>
{% endif %}
```
# 🤝 Contribuye
¿Quieres contribuir? Empieza con estos issues:
- [ ] Crear soporte para rutas dinámicas con parámetros
- [ ] Añadir renderizado condicional avanzado
- [ ] Mejorar documentación del motor de plantillas
