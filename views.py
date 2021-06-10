from framewrk.templator import render
from patterns.creational_patterns import Engine, Logger


site = Engine()
logger = Logger('main')


class Index:
    def __call__(self, request):
        #return '200 OK', render('index.html', username=request.get('username', None))
        return "200 OK", render("index.html", objects_list=site.categories, username=request.get('username', None))


class About:
    def __call__(self, request):
        return '200 OK', render('about.html')


class Price:
    def __call__(self, request):
        return '200 OK', render('price.html', date=request.get('date', None))


class Feedback:
    def __call__(self, request):
        return '200 OK', render('feedback.html')


class CoursesList:
    def __call__(self, request):
        logger.log("Список курсов")
        category_id = int(request['request_params']['id'])
        logger.log(f"ID категоии {category_id}")
        try:
            category = site.find_category_by_id(category_id)
            return '200 OK', render('course-list.html', objects_list=category.courses, name=category.name, id=category.id)
        except KeyError:
            return '200 OK', 'No curses'


class CreateCourse:
    category_id = -1

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


class CreateCategory:
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


class CategoryList:
    def __call__(self, request):
        logger.log('Список категорий')
        return '200 OK', render('category-list.html', objects_list=site.categories)


class CopyCourse:
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
