from framewrk.templator import render
from patterns.behavioral_patterns import EmailNotifier, SmsNotifier, ListView, CreateView, BaseSerializer
from patterns.creational_patterns import Engine, Logger, MapperRegistry
from patterns.structural_patterns import RouteAdd, Debug
from patterns.architectural_patterns_unit_of_work import UnitOfWork

site = Engine()
logger = Logger('main')
routes = {}
email_notifier = EmailNotifier()
sms_notifier = SmsNotifier()
UnitOfWork.new_current()
UnitOfWork.get_current().set_mapper_registry(MapperRegistry)


@RouteAdd(routes=routes, url="/")
class Index:
    @Debug(name="Index")
    def __call__(self, request):
        return "200 OK", render("index.html", objects_list=site.categories, username=request.get('username', None))


@RouteAdd(routes=routes, url="/about/")
class About:
    @Debug(name="About")
    def __call__(self, request):
        return '200 OK', render('about.html')


@RouteAdd(routes=routes, url="/price/")
class Price:
    @Debug(name="Price")
    def __call__(self, request):
        return '200 OK', render('price.html', date=request.get('date', None))


@RouteAdd(routes=routes, url="/feedback/")
class Feedback:
    @Debug(name="Feedback")
    def __call__(self, request):
        return '200 OK', render('feedback.html')


@RouteAdd(routes=routes, url="/course-list/")
class CoursesList:
    @Debug(name="CoursesList")
    def __call__(self, request):
        logger.log("Список курсов")
        category_id = int(request['request_params']['id'])
        logger.log(f"ID категоии {category_id}")
        try:
            category = site.find_category_by_id(category_id)
            return '200 OK', render('course-list.html', objects_list=category.courses, name=category.name,
                                    id=category.id)
        except KeyError:
            return '200 OK', 'No curses'


@RouteAdd(routes=routes, url="/course-new/")
class CreateCourse:
    category_id = -1

    @Debug(name="CreateCourse")
    def __call__(self, request):
        print(request)
        if request['method'] == 'POST':
            # метод пост
            data = request['data']

            name = data['name']
            name = site.decode_value(name)

            category = None
            if self.category_id != -1:
                category = site.find_category_by_id(int(self.category_id))

                course = site.create_course('record', name, category)
                course.observers.append(email_notifier)
                course.observers.append(sms_notifier)
                site.courses.append(course)

            return '200 OK', render('course-list.html', objects_list=category.courses,
                                    name=category.name, id=category.id)

        else:
            try:
                self.category_id = int(request['request_params']['id'])
                category = site.find_category_by_id(int(self.category_id))

                return '200 OK', render('create-course.html', name=category.name, id=category.id)
            except KeyError:
                return '200 OK', 'Empty category'


@RouteAdd(routes=routes, url="/category-new/")
class CreateCategory:
    @Debug(name="CreateCategory")
    def __call__(self, request):
        if request['method'] == 'POST':
            # метод пост
            print(request)
            data = request['data']

            name = data['name']
            name = site.decode_value(name)

            category_id = data.get('category_id')

            category = None
            if category_id:
                category = site.find_category_by_id(int(category_id))

            new_category = site.create_category(name, category)

            site.categories.append(new_category)

            return '200 OK', render('index.html', objects_list=site.categories)
        else:
            categories = site.categories
            return '200 OK', render('category-new.html', categories=categories)


@Debug(name="CategoryList")
class CategoryList:
    @Debug(name="CategoryList")
    def __call__(self, request):
        logger.log('Список категорий')
        return '200 OK', render('category-list.html', objects_list=site.categories)


@RouteAdd(routes=routes, url="/copy-course/")
class CopyCourse:
    @Debug(name="CopyCourse")
    def __call__(self, request):
        request_params = request['request_params']

        try:
            name = request_params['name']
            old_course = site.get_course(name)
            if old_course:
                new_name = f'copy_{name}'
                new_course = old_course.clone()
                new_course.name = new_name
                site.courses.append(new_course)

            return '200 OK', render('course-list.html', objects_list=site.courses)
        except KeyError:
            return '200 OK', 'No courses have been added yet'


@RouteAdd(routes=routes, url='/student-list/')
class StudentListView(ListView):
    queryset = site.students
    template_name = 'student-list.html'


@RouteAdd(routes=routes, url='/create-student/')
class StudentCreateView(CreateView):
    template_name = 'create-student.html'

    def create_obj(self, data: dict):
        name = data['name']
        name = site.decode_value(name)
        new_obj = site.create_user('student', name)
        site.students.append(new_obj)


@RouteAdd(routes=routes, url='/add-student/')
class AddStudentByCourseCreateView(CreateView):
    template_name = 'add-student.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['courses'] = site.courses
        context['students'] = site.students
        return context

    def create_obj(self, data: dict):
        course_name = data['course_name']
        course_name = site.decode_value(course_name)
        course = site.get_course(course_name)
        student_name = data['student_name']
        student_name = site.decode_value(student_name)
        student = site.get_student(student_name)
        course.add_student(student)


@RouteAdd(routes=routes, url='/api/')
class CourseApi:
    @Debug(name='CourseApi')
    def __call__(self, request):
        return '200 OK', BaseSerializer(site.courses).save()
