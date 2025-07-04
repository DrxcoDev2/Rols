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