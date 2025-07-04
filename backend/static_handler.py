import os
import mimetypes
from urllib.parse import unquote
from pathlib import Path

class StaticFileHandler:
    def __init__(self, static_dir='static'):
        # Asegurarse que el directorio static existe
        self.static_dir = Path(static_dir)
        self.static_dir.mkdir(exist_ok=True)
        
        # Asegurarse que los subdirectorios existen
        for subdir in ['css', 'js', 'images']:
            (self.static_dir / subdir).mkdir(exist_ok=True)
        
        # Inicializar tipos MIME
        self.initialize_mime_types()
    
    def initialize_mime_types(self):
        """A�adir tipos MIME adicionales si son necesarios"""
        mimetypes.init()
        # A�adir tipos personalizados si no est�n en la lista por defecto
        if not mimetypes.guess_type('.js')[0]:
            mimetypes.add_type('application/javascript', '.js')
        if not mimetypes.guess_type('.css')[0]:
            mimetypes.add_type('text/css', '.css')
    
    def is_safe_path(self, path):
        """Verifica que el path solicitado es seguro y no sale del directorio static"""
        try:
            requested_path = (self.static_dir / path).resolve()
            common_prefix = os.path.commonprefix([requested_path, self.static_dir.resolve()])
            return str(self.static_dir.resolve()) == common_prefix
        except (ValueError, TypeError):
            return False
    
    async def handle_static_request(self, path):

        # Decodificar la URL y limpiar el path
        clean_path = unquote(path).lstrip('/')
        
        # Verificar que el path es seguro
        if not self.is_safe_path(clean_path):
            return None
        
        file_path = self.static_dir / clean_path
        
        # Verificar si el archivo existe
        if not file_path.is_file():
            return None
            
        # Obtener el tipo MIME
        content_type, encoding = mimetypes.guess_type(str(file_path))
        if not content_type:
            content_type = 'application/octet-stream'
            
        # Leer el archivo
        try:
            with open(file_path, 'rb') as f:
                content = f.read()
                
            headers = {
                'Content-Type': content_type,
                'Content-Length': len(content),
                'Cache-Control': 'public, max-age=3600'  # Cache por 1 hora
            }
            
            if encoding:
                headers['Content-Encoding'] = encoding
                
            return headers, content
            
        except IOError:
            return None