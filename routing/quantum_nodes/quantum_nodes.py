from __future__ import annotations

import json

from pathlib import Path
from dataclasses import dataclass
from typing import Dict, List

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


def _parse_node_json(node_json: str):
    node_json = json.loads(node_json)['nodes']

    nodes: Dict[str, Node] = {}
    # Step through and create all nodes and inputs
    for jnode in node_json.values():
        node = Node(name=jnode['name'], inputs={}, outputs=[])
        for input_id in jnode['inputs']:
            node.inputs[input_id] = Input(input_id, node)
        nodes[jnode['id']] = node

    # Step through and connect all outputs
    for jnode in node_json.values():
        node = nodes[jnode['id']]
        for output_id, joutput in jnode['outputs'].items():
            connections = joutput['connections']
            if len(connections) == 0:
                continue
            node_id = connections[0]['node']
            node_in = connections[0]['input']
            target = nodes[node_id].inputs[node_in]
            node.outputs.append(Output(output_id, target))

    return nodes


def _create_circuit_from_nodes(nodes: Dict[str, Node]):
    return 'TODO: create circuit'


async def create_quantum_diagram(request):
    if 'node_json' not in request.form:
        raise InvalidUsage(
            'route requires that a "node_json" argument be sent the form')

    nodes = _parse_node_json(request.form['node_json'][0])
    return response.json({'circuit': _create_circuit_from_nodes(nodes)})
