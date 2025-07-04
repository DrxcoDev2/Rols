from backend.server import HTTPServer
import asyncio

server = HTTPServer(static_dir='static')

@server.route('/')
async def index():
    return '''
    <html>
        <head>
            <link rel="stylesheet" href="/static/css/style.css">
            <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
        </head>
        <body id="app" style="background: white">
            
            <div class="flex justify-center">Welcome to Rols</div>
            
        </body>
    </html>
    '''

if __name__ == '__main__':
    asyncio.run(server.run())
