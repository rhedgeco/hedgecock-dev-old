from re import sub
from sanic.exceptions import InvalidUsage
from sanic.response import text
from sanic.views import HTTPMethodView

from backend.quantum_blocks.quantum_exec import scoped_exec


class QuantumBlocks(HTTPMethodView):
    async def post(self, request):
        if 'code' not in request.form:
            raise InvalidUsage('there must be a "code" argument in the form')

        code = str(request.form['code'][0])
        code = sub(r'import.*|from.*', '', code)

        scoped_exec(code)
        return text(code)
