from pathlib import Path
from sanic import Sanic, response

import routing.ice_cream_or_pickle.ice_cream_or_pickle as ice_cream_or_pickle
import routing.quantum_nodes.quantum_nodes as quantum_nodes


def add_routes(app: Sanic):
    # create handler for index route
    home_index = Path('./home_index')

    async def index(request):
        return await response.file(str(home_index / 'index.html'))

    async def favicon(request):
        return await response.file(str(home_index / 'favicon.ico'))

    app.static('/static', str(home_index / 'static'))
    app.add_route(index, '/')
    app.add_route(favicon, '/favicon.ico')

    # Ice cream or pickle
    app.add_route(ice_cream_or_pickle.IceCreamOrPickle.as_view(),
                  '/ice_cream_or_pickle')

    # Quantum node designer
    quantum_nodes_path = Path('./routing') / 'quantum_nodes'
    app.static('/quantum_nodes/static',
               str((quantum_nodes_path / 'static').absolute()))
    app.add_route(quantum_nodes.designer, '/quantum_nodes')
    app.add_route(quantum_nodes.designer, '/quantum_nodes/designer')
    app.add_route(quantum_nodes.create_quantum_diagram,
                  '/quantum_nodes/create', ['POST'])
