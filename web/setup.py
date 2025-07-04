import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.server import HTTPServer
import asyncio

server = HTTPServer(static_dir='../static')

@server.route('/')
async def index():
    return '''
    <html>
        <head>
            <link rel="stylesheet" href="/static/css/style.css">
            <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
        </head>
        <body id="app" style="background: white">
            
            <nav class="">
                <h1 class="">Rols</h1>
            </nav>
            
        </body>
    </html>
    '''

if __name__ == '__main__':
    asyncio.run(server.run())
