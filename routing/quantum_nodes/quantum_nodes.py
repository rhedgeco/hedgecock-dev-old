from pathlib import Path

from sanic import response


async def designer(request):
    uri = request.uri_template
    if uri == '/quantum_nodes/designer':
        return await response.file(
            str(Path('routing') / 'quantum_nodes' / 'designer.html'))
    else:
        return response.redirect('/quantum_nodes/designer')
