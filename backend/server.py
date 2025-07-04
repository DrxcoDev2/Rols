import asyncio
import re
import uuid
import urllib.parse
import json
from http.cookies import SimpleCookie
from .static_handler import StaticFileHandler  
from inspect import signature
from typing import Dict, Any, Optional, Tuple

MAX_REQUEST_SIZE = 65536  
sessions: Dict[str, dict] = {}

class HTTPResponse:
    def __init__(
        self, 
        body: Any = "", 
        status: str = "200 OK",
        content_type: str = "text/html",
        headers: Optional[Dict[str, str]] = None
    ):
        self.body = body
        self.status = status
        self.content_type = content_type
        self.headers = headers or {}

    def encode(self, session_id: Optional[str] = None) -> bytes:
        if isinstance(self.body, str):
            body_bytes = self.body.encode()
        else:
            body_bytes = self.body  

        headers = [
            f"HTTP/1.1 {self.status}",
            f"Content-Type: {self.content_type}",
            f"Content-Length: {len(body_bytes)}"
        ]
        
        if session_id:
            headers.append(f"Set-Cookie: sessionid={session_id}; HttpOnly; Path=/")
        
        for key, value in self.headers.items():
            headers.append(f"{key}: {value}")
        
        header_bytes = "\r\n".join(headers).encode() + b"\r\n\r\n"
        return header_bytes + body_bytes

class HTTPServer:
    def __init__(self, host: str = '127.0.0.1', port: int = 8000, static_dir: str = 'static'):
        self.host = host
        self.port = port
        self.routes = []
        self.static_handler = StaticFileHandler(static_dir)

    def route(self, path: str, methods: Optional[list] = None):
        if methods is None:
            methods = ['GET']

        def decorator(handler):
            pattern = re.sub(r':([^/]+)', r'(?P<\1>[^/]+)', path)
            self.routes.append({
                'pattern': re.compile(f'^{pattern}$'),
                'handler': handler,
                'methods': methods
            })
            print(f"Ruta registrada: {methods[0]} ^{path}$")
            return handler
        return decorator

    def parse_request(self, request_text: str) -> Tuple[dict, str]:
        headers_raw, _, body = request_text.partition('\r\n\r\n')
        headers_lines = headers_raw.splitlines()[1:]  
        
        headers = {}
        for line in headers_lines:
            if ':' in line:
                key, value = line.split(':', 1)
                headers[key.strip().lower()] = value.strip()
        
        return headers, body

    def get_session(self, headers: dict) -> Tuple[str, dict]:
        cookies = SimpleCookie()
        if 'cookie' in headers:
            cookies.load(headers['cookie'])
            
        session_id = None
        if 'sessionid' in cookies:
            session_id = cookies['sessionid'].value
            
        if not session_id or session_id not in sessions:
            session_id = str(uuid.uuid4())
            sessions[session_id] = {}
            
        return session_id, sessions[session_id]

    async def parse_body(self, method: str, headers: dict, body: str) -> Optional[Any]:
        if method != 'POST':
            return None
            
        content_type = headers.get('content-type', '')
        
        if 'application/x-www-form-urlencoded' in content_type:
            parsed = urllib.parse.parse_qs(body)
            return {k: v[0] if len(v) == 1 else v for k, v in parsed.items()}
        elif 'application/json' in content_type:
            try:
                return json.loads(body)
            except json.JSONDecodeError:
                return None
        
        return body

    async def handle_static(self, path: str) -> Optional[HTTPResponse]:
        if not path.startswith('/static/'):
            return None
            
        result = await self.static_handler.handle_static_request(path[len('/static/'):])
        if not result:
            return HTTPResponse(
                body="File not found",
                status="404 Not Found",
                content_type="text/plain"
            )
            
        headers, content = result
        content_type = headers.get('Content-Type', 'application/octet-stream')
        return HTTPResponse(
            body=content,
            content_type=content_type,
            headers={k:v for k,v in headers.items() if k.lower() != 'content-type'}
        )

    async def handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        try:
            data = await reader.read(MAX_REQUEST_SIZE)
            request_text = data.decode(errors='ignore')

            if not request_text.strip():
                await self.send_response(writer, HTTPResponse(
                    body="Empty request",
                    status="400 Bad Request",
                    content_type="text/plain"
                ))
                writer.close()
                await writer.wait_closed()
                return

            request_line = request_text.splitlines()[0]
            try:
                method, path, _ = request_line.split()
            except ValueError:
                await self.send_response(writer, HTTPResponse(
                    body="Malformed request line",
                    status="400 Bad Request",
                    content_type="text/plain"
                ))
                writer.close()
                await writer.wait_closed()
                return

            if path.startswith('/static/'):
                static_response = await self.handle_static(path)
                await self.send_response(writer, static_response)
                writer.close()
                await writer.wait_closed()
                return

            headers, body = self.parse_request(request_text)
            session_id, session = self.get_session(headers)

            handler = None
            path_params = {}
            allowed_methods = set()

            for route in self.routes:
                match = route['pattern'].match(path)
                if match:
                    allowed_methods.update(route['methods'])
                    if method in route['methods']:
                        handler = route['handler']
                        path_params = match.groupdict()
                        break

            parsed_body = await self.parse_body(method, headers, body)

            if handler:
                try:
                    handler_params = signature(handler).parameters
                    kwargs = {
                        'session': session,
                        'body': parsed_body,
                        **path_params
                    }
                    kwargs = {k: v for k, v in kwargs.items() if k in handler_params}

                    result = await handler(**kwargs)
                    
                    if isinstance(result, HTTPResponse):
                        response = result
                    elif isinstance(result, tuple):
                        body, status, headers = result + (None,) * (3 - len(result))
                        response = HTTPResponse(body, status or "200 OK", headers=headers)
                    else:
                        response = HTTPResponse(str(result))

                except Exception as e:
                    print(f"[ERROR] En handler: {e}")
                    response = HTTPResponse(
                        body="Internal Server Error",
                        status="500 Internal Server Error",
                        content_type="text/plain"
                    )
            elif allowed_methods:
                response = HTTPResponse(
                    body="Method Not Allowed",
                    status="405 Method Not Allowed",
                    headers={'Allow': ', '.join(allowed_methods)}
                )
            else:
                response = HTTPResponse(
                    body="Not Found",
                    status="404 Not Found",
                    content_type="text/plain"
                )

            await self.send_response(writer, response, session_id)

        except Exception as e:
            print(f'Error handling request: {e}')
        finally:
            writer.close()
            await writer.wait_closed()

    async def send_response(
        self, 
        writer: asyncio.StreamWriter, 
        response: HTTPResponse, 
        session_id: Optional[str] = None
    ):
        writer.write(response.encode(session_id))
        await writer.drain()

    async def run(self):
        print("Rutas registradas:")
        for route in self.routes:
            print(f"{route['methods'][0]} {route['pattern'].pattern}")
            
        server = await asyncio.start_server(
            self.handle_client,
            self.host,
            self.port
        )
        
        print(f"Server running on http://{self.host}:{self.port}")
        
        async with server:
            await server.serve_forever()
