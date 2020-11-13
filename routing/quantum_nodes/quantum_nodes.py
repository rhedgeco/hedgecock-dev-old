from __future__ import annotations

import json

from pathlib import Path
from dataclasses import dataclass
from typing import Dict, Tuple, List

from sanic import response
from sanic.exceptions import InvalidUsage


@dataclass
class Input:
    name: str
    node: Node


@dataclass
class Output:
    name: str
    connection: Input


@dataclass
class Node:
    name: str
    inputs: Dict[str, Input]
    outputs: List[Output]


async def designer(request):
    uri = request.uri_template
    if uri == '/quantum_nodes/designer':
        return await response.file(
            str(Path('routing') / 'quantum_nodes' / 'designer.html'))
    else:
        return response.redirect('/quantum_nodes/designer')


async def create_quantum_diagram(request):
    if 'node_json' not in request.form:
        raise InvalidUsage(
            'route requires that a "node_json" argument be sent the form')

    node_json = json.loads(request.form['node_json'][0])['nodes']

    # # Create all nodes and fill inputs
    # nodes = {}
    # for jnode in node_json.values():
    #     node = Node(name=jnode['name'], inputs={}, outputs=[])
    #     for input in jnode['inputs']:
    #         node.inputs[input['name']] = Input(name=input['name'], node=node)
    #     nodes[jnode['id']] = node
    #
    # # Populate all nodes with output connections
    # for jnode in node_json.values():
    #     node = nodes[jnode['id']]
    #     for key, joutput in jnode['outputs'].items():
    #         joutput = joutput['connections'][0]
    #         input = nodes[joutput['node']].inputs[joutput['input']]
    #         node.outputs.append(Output(key, input))
    #
    # print(nodes)


    return response.json({
        'circuit': 'TODO: Create circuit'
    })
