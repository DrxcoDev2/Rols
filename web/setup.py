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

            <link rel="preconnect" href="https://fonts.googleapis.com">
            <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
            <link href="https://fonts.googleapis.com/css2?family=Cascadia+Code:ital,wght@0,200..700;1,200..700&family=Poppins:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&family=Roboto:ital,wght@0,100..900;1,100..900&display=swap" rel="stylesheet">
        </head>
        <body id="app" style="background: white; font-family: 'Roboto', sans-serif">

            
            <nav class="p-4 justify-between flex bg-red-400 text-gray-100">
                <h1 class="text-xl">Rols</h1>
                <div class="space-x-4">
                    <a href="" class="">Blog</a>
                    <a href="" class="">Repo</a>
                </div>
            </nav>

            <div class="flex mt-26 justify-center">
                <div class="">
                    <h1 class="text-6xl font-light">The Innovation web in Python</h1>
                    <h1 class="text-6xl font-light flex justify-center">For you projects</h1>
                    <p class="flex justify-center max-w-[800px] text-center text-lg text-gray-700 py-10">
                        Rols is a web micro-framework built in pure Python, designed to handle both the backend and frontend using a simple, fast, and extensible architecture.
                    </p>
                    <div class="grid lg:grid-cols-2 gap-x-4 justify-center p-4 max-w-[320px] mx-auto">
                        <a href="" class="p-2 border border-red-400 max-w-[150px] border-2 rounded-lg text-center">Read docs</a>
                        <a href="" class="p-2 border border-red-400 max-w-[150px] border-2 rounded-lg text-center text-gray-100 bg-red-400">Use</a>
                    </div>


                </div>
                
            </div>
            
        </body>
    </html>
    '''

if __name__ == '__main__':
    asyncio.run(server.run())
