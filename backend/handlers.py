from templates import SimpleTemplate
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')

async def index():
    tpl = SimpleTemplate(os.path.join(TEMPLATE_DIR, 'index.html'))
    html = tpl.render({'name': 'Jack'})
    return html
