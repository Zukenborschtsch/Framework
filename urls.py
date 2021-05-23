from datetime import date

from views import Index, About, Price, Feedback

routes = {
    '/': Index(),
    '/about/': About(),
    '/price/': Price(),
    '/feedback/': Feedback()
}


def date_front(request):
    request['date'] = date.today()


def user_front(request):
    request['username'] = 'user'


fronts = [date_front, user_front]
