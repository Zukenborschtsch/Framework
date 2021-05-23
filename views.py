from framewrk.templator import render


class Index:
    def __call__(self, request):
        return '200 OK', render('index.html', username=request.get('username', None))


class About:
    def __call__(self, request):
        return '200 OK', render('about.html')


class Price:
    def __call__(self, request):
        return '200 OK', render('price.html', date=request.get('date', None))


class Feedback:
    def __call__(self, request):
        return '200 OK', render('feedback.html')
