from datetime import date


def date_front(request):
    request['date'] = date.today()


def user_front(request):
    request['username'] = 'user'


fronts = [date_front, user_front]
