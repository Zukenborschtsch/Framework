from jinja2 import FileSystemLoader
from jinja2.environment import Environment


def render(template_name, folder='templates', **kwargs):
    context = Environment()
    context.loader = FileSystemLoader(folder)
    template = context.get_template(template_name)
    print(template)

    return template.render(**kwargs)
