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
    connection: Output = None


@dataclass
class Output:
    name: str
    node: Node
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

    output_node = None
    nodes: Dict[str, Node] = {}
    # Step through and create all nodes and inputs
    for jnode in node_json.values():
        node = Node(name=jnode['name'], inputs={}, outputs=[])
        for input_id in jnode['inputs']:
            node.inputs[input_id] = Input(input_id, node)
        nodes[jnode['id']] = node
        if node.name == 'Circuit Output':
            if output_node is not None:
                raise InvalidUsage('There must be only one circuit output.')
            output_node = node

    if output_node is None:
        raise InvalidUsage('There must one circuit output.')

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
            out = Output(output_id, node, target)
            target.connection = out
            node.outputs.append(out)

    return output_node


def _create_circuit_from_nodes(output_node: Node):
    assert output_node.name == 'Circuit Output'

    return 'TODO: parse circuit diagram to quantum algorithm'


async def create_quantum_diagram(request):
    if 'node_json' not in request.form:
        raise InvalidUsage(
            'route requires that a "node_json" argument be sent the form')

    output_node = _parse_node_json(request.form['node_json'][0])
    return response.json({'circuit': _create_circuit_from_nodes(output_node)})
