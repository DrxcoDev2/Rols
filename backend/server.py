import asyncio
import re
from handlers import index

class HTTPServer:
    def __init__(self, host='127.0.0.1', port=8000):
        self.host = host
        self.port = port
        self.routes = []

    def route(self, path_pattern, method='GET'):
        pattern = '^' + re.sub(r'{(\w+)}', r'(?P<\1>[^/]+)', path_pattern) + '$'
        regex = re.compile(pattern)
        def decorator(func):
            self.routes.append({'method': method.upper(), 'pattern': regex, 'handler': func})
            return func
        return decorator

    async def handle_client(self, reader, writer):
        data = await reader.read(65536)
        request_text = data.decode(errors='ignore')
        request_line = request_text.splitlines()[0]
        method, path, _ = request_line.split()

        handler = None
        path_params = {}

        for route in self.routes:
            if route['method'] == method:
                match = route['pattern'].match(path)
                if match:
                    handler = route['handler']
                    path_params = match.groupdict()
                    break

        if handler:
            response_body = await handler(**path_params)
            response = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/html\r\n"
                f"Content-Length: {len(response_body.encode())}\r\n"
                "\r\n"
                f"{response_body}"
            )
        else:
            response = "HTTP/1.1 404 Not Found\r\n\r\nRoute not found"

        writer.write(response.encode())
        await writer.drain()
        writer.close()

    async def run(self):
        print("Rutas registradas:")
        for route in self.routes:
            print(f"{route['method']} {route['pattern'].pattern}")
        server = await asyncio.start_server(self.handle_client, self.host, self.port)
        print(f"Server running on http://{self.host}:{self.port}")
        async with server:
            await server.serve_forever()

server = HTTPServer()

# Registrar rutas
server.route("/", method="GET")(index)

import asyncio
asyncio.run(server.run())
