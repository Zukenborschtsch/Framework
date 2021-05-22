from wsgiref.simple_server import make_server
from urls import routes, fronts
from framewrk.main import Framework

app = Framework(routes, fronts)

with make_server("", 8080, app) as httpd:
    print("Запуск на порту 8080...")
    httpd.serve_forever()