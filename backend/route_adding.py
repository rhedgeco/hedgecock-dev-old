from pathlib import Path

from sanic import Sanic

from backend.ice_cream_or_pickle.ice_cream_or_pickle import IceCreamOrPickle
from backend.quantum_blocks.quantum_blocks import QuantumBlocks


def add_routes(app: Sanic, frontend_dir: Path):
    app.static('/', str(frontend_dir))
    app.add_route(IceCreamOrPickle.as_view(), '/ice_cream_or_pickle')
    app.add_route(QuantumBlocks().as_view(),
                  '/projects/quantum_blocks/submit_code')
