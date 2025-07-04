import mimetypes
from urllib.parse import unquote
from pathlib import Path
import aiofiles  # Debes instalarlo: pip install aiofiles

class StaticFileHandler:
    def __init__(self, static_dir='static'):
        self.static_dir = Path(static_dir).resolve()
        self.static_dir.mkdir(exist_ok=True)
        
        for subdir in ['css', 'js', 'images']:
            (self.static_dir / subdir).mkdir(exist_ok=True)
        
        self._initialize_mime_types()
    
    def _initialize_mime_types(self):
        mimetypes.init()
        if not mimetypes.guess_type('.js')[0]:
            mimetypes.add_type('application/javascript', '.js')
        if not mimetypes.guess_type('.css')[0]:
            mimetypes.add_type('text/css', '.css')
    
    def _is_safe_path(self, path: str) -> bool:
        try:
            requested_path = (self.static_dir / path).resolve()
            # Verifica que requested_path est� dentro de self.static_dir
            return self.static_dir == requested_path or self.static_dir in requested_path.parents
        except (ValueError, TypeError):
            return False
    
    async def handle_static_request(self, path: str):
        clean_path = unquote(path).lstrip('/')
        
        if not self._is_safe_path(clean_path):
            return None
        
        file_path = self.static_dir / clean_path
        
        if not file_path.is_file():
            return None
        
        content_type, encoding = mimetypes.guess_type(str(file_path))
        if not content_type:
            content_type = 'application/octet-stream'
        
        try:
            async with aiofiles.open(file_path, 'rb') as f:
                content = await f.read()
            
            headers = {
                'Content-Type': content_type,
                'Content-Length': str(len(content)),
                # Para desarrollo evita cache; cambia a 'public, max-age=3600' para producci�n
                'Cache-Control': 'no-store, no-cache, must-revalidate, max-age=0',
            }
            
            if encoding:
                headers['Content-Encoding'] = encoding
            
            return headers, content
        
        except IOError:
            return None
