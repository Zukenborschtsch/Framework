from wsgiref.simple_server import make_server

from framewrk.main import Framework
from urls import routes, fronts

app = Framework(routes, fronts)

with make_server('', 8080, app) as httpd:
    print('Запуск на порту 8080...')
    httpd.serve_forever()
