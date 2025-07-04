from templates import SimpleTemplate
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')


async def index(body=None, session=None, **kwargs):
    visit_count = session.get('visit_count', 0)
    visit_count += 1
    session['visit_count'] = visit_count

    tpl = SimpleTemplate(os.path.join(TEMPLATE_DIR, 'index.html'))
    html = tpl.render({
        'name': 'Jack',
        'visit_count': visit_count,
        'age': 20,
        'items': ['manzana', 'pera', 'naranja']
    })
    return html

async def login(body=None, session=None, **kwargs):
    username = body.get('username') if body else None
    password = body.get('password') if body else None

    tpl = SimpleTemplate(os.path.join(TEMPLATE_DIR, 'login_response.html'))

    if username == 'admin' and password == '1234':
        session['user'] = username  
        html = tpl.render({'message': f'Login exitoso, bienvenido {username}'})
    else:
        html = tpl.render({'message': 'Credenciales incorrectas'})
    return html
