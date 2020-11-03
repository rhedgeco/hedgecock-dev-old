import base64
import random

from sanic import response
from sanic.views import HTTPMethodView
from jinja2 import Template


class IceCreamOrPickle(HTTPMethodView):
    # noinspection PyMethodMayBeStatic
    def get(self, request):
        num = random.randint(0, 1)
        data_path = 'backend/ice_cream_or_pickle/data'

        html = open(f'{data_path}/ice_cream.html'
                    if num == 0 else
                    f'{data_path}/pickle.html', 'r').read()

        return response.html(html)

    # noinspection PyMethodMayBeStatic
    def template_render(self):
        num = random.randint(0, 1)
        data_path = 'backend/ice_cream_or_pickle/data'

        html_f = open(f'{data_path}/ice_cream_or_pickle.html', 'r')
        html_data = Template(html_f.read())
        html_f.close()

        title = "Ice Cream" if num == 0 else "Pickle"

        img_f = open(
            f'{data_path}/{"ice_cream" if num == 0 else "pickle"}.png',
            'rb')
        img = base64.b64encode(img_f.read())
        img = f'{img}'[2:-1]
        img_f.close()

        color = "#f1ecc4" if num == 0 else "#79c263"

        html_data = html_data.render(title=title, image_data=img, color=color)

        return html_data
