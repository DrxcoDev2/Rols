import asyncio
import re

class HTTPServer:
    def __init__(self, host='127.0.0.1', port=8000):
        self.host = host
        self.port = port
        self.routes = []

    def route(self, path_pattern, method='GET'):
        # Convierte la ruta con {param} en expresi�n regular
        pattern = '^' + re.sub(r'{(\w+)}', r'(?P<\1>[^/]+)', path_pattern) + '$'
        regex = re.compile(pattern)

        def decorator(func):
            self.routes.append({
                'method': method.upper(),
                'pattern': regex,
                'handler': func
            })
            return func
        return decorator

    async def handle_client(self, reader, writer):
        data = await reader.read(1024)
        request_text = data.decode()
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
        server = await asyncio.start_server(self.handle_client, self.host, self.port)
        print(f"Server running on http://{self.host}:{self.port}")
        async with server:
            await server.serve_forever()


if __name__ == '__main__':
    server = HTTPServer()

    @server.route("/user/{user_id}", method="GET")
    async def get_user(user_id):
        return f"<h1>Usuario: {user_id}</h1>"

    @server.route("/product/{category}/{product_id}", method="GET")
    async def get_product(category, product_id):
        return f"<h1>Producto {product_id} en categoría {category}</h1>"

    import asyncio
    asyncio.run(server.run())
