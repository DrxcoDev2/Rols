import asyncio
import re
import uuid
import urllib.parse
import json

MAX_REQUEST_SIZE = 65536

def parse_cookies(cookie_header: str) -> dict:
    cookies = {}
    if not cookie_header:
        return cookies
    pairs = cookie_header.split(';')
    for pair in pairs:
        if '=' in pair:
            k, v = pair.strip().split('=', 1)
            cookies[k] = v
    return cookies

sessions = {}

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
        try:
            data = await reader.read(MAX_REQUEST_SIZE)
            request_text = data.decode(errors='ignore')

            if not request_text.strip():
                writer.close()
                await writer.wait_closed()
                return

            lines = request_text.splitlines()
            if not lines:
                response = "HTTP/1.1 400 Bad Request\r\n\r\nEmpty request"
                writer.write(response.encode())
                await writer.drain()
                return

            request_line = lines[0]
            parts = request_line.split()
            if len(parts) < 3:
                response = "HTTP/1.1 400 Bad Request\r\n\r\nMalformed request line"
                writer.write(response.encode())
                await writer.drain()
                return
            method, path, _ = parts

            headers, _, body = request_text.partition('\r\n\r\n')
            headers_lines = headers.splitlines()[1:]
            headers_dict = {}
            for line in headers_lines:
                if ':' in line:
                    k, v = line.split(':', 1)
                    headers_dict[k.strip().lower()] = v.strip()

            cookie_header = headers_dict.get('cookie')
            cookies = parse_cookies(cookie_header)
            session_id = cookies.get('sessionid')
            if session_id is None or session_id not in sessions:
                session_id = str(uuid.uuid4())
                sessions[session_id] = {}

            session = sessions[session_id]

            handler = None
            path_params = {}
            allowed_methods = set()
            for route in self.routes:
                match = route['pattern'].match(path)
                if match:
                    allowed_methods.add(route['method'])
                    if route['method'] == method:
                        handler = route['handler']
                        path_params = match.groupdict()
                        break

            parsed_body = None
            if method == 'POST':
                content_type = headers_dict.get('content-type', '')
                if 'application/x-www-form-urlencoded' in content_type:
                    parsed_body = urllib.parse.parse_qs(body)
                    parsed_body = {k: v[0] if len(v) == 1 else v for k, v in parsed_body.items()}
                elif 'application/json' in content_type:
                    try:
                        parsed_body = json.loads(body)
                    except:
                        parsed_body = None
                else:
                    parsed_body = body

            if handler:
                try:
                    result = await handler(**path_params, body=parsed_body, session=session)
                    if isinstance(result, tuple):
                        response_body, status, custom_headers = result + (None,) * (3 - len(result))
                        status = status or "200 OK"
                        custom_headers = custom_headers or []
                    else:
                        response_body = result
                        status = "200 OK"
                        custom_headers = []
                    response_headers = [
                        f"HTTP/1.1 {status}",
                        "Content-Type: text/html",
                        f"Set-Cookie: sessionid={session_id}; HttpOnly; Path=/",
                        f"Content-Length: {len(response_body.encode())}"
                    ] + custom_headers
                    response = "\r\n".join(response_headers) + "\r\n\r\n" + response_body
                except Exception as handler_error:
                    print(f"[ERROR] En handler: {handler_error}")
                    response = (
                        "HTTP/1.1 500 Internal Server Error\r\n"
                        "Content-Type: text/plain\r\n"
                        "\r\n"
                        "Internal Server Error"
                    )
            elif allowed_methods:
                response = (
                    "HTTP/1.1 405 Method Not Allowed\r\n"
                    f"Allow: {', '.join(allowed_methods)}\r\n"
                    "\r\n"
                    "Method Not Allowed"
                )
            else:
                response = "HTTP/1.1 404 Not Found\r\n\r\nRoute not found"

            writer.write(response.encode())
            await writer.drain()
        except Exception as general_error:
            print(f"[ERROR] En el servidor: {general_error}")
        finally:
            writer.close()
            await writer.wait_closed()

    async def run(self):
        print("Rutas registradas:")
        for route in self.routes:
            print(f"{route['method']} {route['pattern'].pattern}")
        server = await asyncio.start_server(self.handle_client, self.host, self.port)
        print(f"Server running on http://{self.host}:{self.port}")
        async with server:
            await server.serve_forever()