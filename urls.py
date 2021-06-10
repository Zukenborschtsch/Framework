from datetime import date

from views import Index, About, Price, Feedback, CreateCourse, CoursesList, CreateCategory, CategoryList, CopyCourse

routes = {
    '/': Index(),
    '/about/': About(),
    '/price/': Price(),
    '/feedback/': Feedback(),
    "/course-new/": CreateCourse(),
    "/course-list/": CoursesList(),
    "/category-new/": CreateCategory(),
    "/category-list/": CategoryList(),
    "/copy-course/": CopyCourse()
}


def date_front(request):
    request['date'] = date.today()


def user_front(request):
    request['username'] = 'user'


fronts = [date_front, user_front]
