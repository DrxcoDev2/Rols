from backend.server import HTTPServer
import asyncio

server = HTTPServer(static_dir='static')

@server.route('/')
async def index():
    return '''
    <html>
        <head>
            <link rel="stylesheet" href="/static/css/style.css">
        </head>
        <body id="app" style="background: white">
            
            <div class="">Welcome to Rols</div>
            
        </body>
    </html>
    '''

if __name__ == '__main__':
    asyncio.run(server.run())
