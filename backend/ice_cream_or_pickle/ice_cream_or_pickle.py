import base64
import random

from sanic import response
from sanic.views import HTTPMethodView
from jinja2 import Template


class IceCreamOrPickle(HTTPMethodView):
    def get(self, request):
        num = random.randint(0, 1)
        data_path = 'backend/ice_cream_or_pickle/data'

        html = Template(
            open(f'{data_path}/ice_cream_or_pickle.html', 'r').read())

        title = "Ice Cream" if num == 0 else "Pickle"

        img = open(f'{data_path}/{"ice_cream" if num == 0 else "pickle"}.png',
                   'rb').read()
        img = base64.b64encode(img)
        img = f'{img}'[2:-1]

        color = "#f1ecc4" if num == 0 else "#79c263"

        html = html.render(title=title, image_data=img, color=color)
        return response.html(html)
