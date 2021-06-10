import quopri
import json
from framewrk.requests import get_req, post_req
from patterns.creational_patterns import Logger


logger = Logger("main")


class PageNotFound404:
    def __call__(self, request):
        return "404 Not Found", "404 Not Found"


class Framework:
    def __init__(self, routes_obj, fronts_obj):
        self.routes_lst = routes_obj
        self.fronts_lst = fronts_obj

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']

        if not path.endswith('/'):
            path = f'{path}/'

        logger.log(path)

        request = {}
        method = environ["REQUEST_METHOD"]
        request["method"] = method

        if environ['REQUEST_METHOD'] == 'GET':
            data = get_req(environ)
            request["request_params"] = data
            print(f'Получен get запрос {data}')

        if method == "POST":
            data = post_req(environ)
            request["data"] = data
            norm_data = decode_mime(data)
            write_file(norm_data)
            print(f'Получен post запрос {norm_data}')

        if path in self.routes_lst:
            view = self.routes_lst[path]
        else:
            view = PageNotFound404()

        for front in self.fronts_lst:
            front(request)

        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]


def write_file(data):
    with open('feedback.json', 'a', encoding='UTF-8') as feed_file:
        json.dump(data, feed_file, ensure_ascii=False, indent=4)


def decode_mime(data):
    ret_data = {}
    for param, value in data.items():
        normalize_value = bytes(
            value.replace('%', '=').replace('+', ' '), "UTF-8"
        )
        decoded_value = quopri.decodestring(normalize_value).decode("UTF-8")
        ret_data[param] = decoded_value
    return ret_data
