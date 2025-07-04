"""
use client
use @backend 
"""

from backend.server import HTTPServer
from backend.templates import SimpleTemplate

server = HTTPServer()

@server.route("/", method="GET")
async def home(body=None, session=None, **kwargs):
    tpl = SimpleTemplate("templates/index.html")
    return tpl.render({'user': session.get('user', 'Invitado')})

@server.route("/login", method="POST")
async def login(body=None, session=None, **kwargs):
    username = body.get('username')
    password = body.get('password')
    if username == 'admin' and password == '1234':
        session['user'] = username
        return "Login OK"
    return "Login fallido"

if __name__ == "__main__":
    import asyncio
    asyncio.run(server.run())
