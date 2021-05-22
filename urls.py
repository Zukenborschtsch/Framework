from datetime import date

from views import Index, About, Price

routes = {
    "/": Index(),
    "/about/": About(),
    "/price/": Price(),
}


def date_front(request):
    request["date"] = date.today()


def user_front(request):
    request["username"] = "user"


fronts = [date_front, user_front]
