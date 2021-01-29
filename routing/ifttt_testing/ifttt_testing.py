import os

from sanic import response
from sanic.views import HTTPMethodView


class IftttTesting(HTTPMethodView):
    @staticmethod
    async def status(request):
        return response.text('ONLINE!')

    @staticmethod
    async def test_setup(request):
        json = {
            'data': {
                'test': 'info'
            }
        }
        return response.json(json)
