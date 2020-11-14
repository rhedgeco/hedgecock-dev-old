const qBitSocket = new Rete.Socket('Quantum Bit');
const cBitSocket = new Rete.Socket('Classical Bit');

function qbitInOut(node, i) {
    var bit = 'qbit';
    if (i > 0 && i !== null) bit = bit + '-' + i;
    var qin = new Rete.Input(bit, bit, qBitSocket, false);
    var qout = new Rete.Output(bit, bit, qBitSocket, false);
    node.addInput(qin);
    node.addOutput(qout);
}

class QuantumCircuit extends Rete.Node {
    constructor(qbits) {
        super('Quantum Circuit');
        for (var i = 0; i < qbits; i++) {
            var qout = new Rete.Output('qbit' + i, 'qbit-' + i, qBitSocket, false);
            this.addOutput(qout);
        }
    }
}

class HadamardGate extends Rete.Node {
    constructor() {
        super('Hadamard Gate');
        qbitInOut(this);
    }
}

class ControlledX extends Rete.Node {
    constructor() {
        super('Controlled X');
        var contIn = new Rete.Input('qbit-0', 'control in', qBitSocket, false);
        var contOut = new Rete.Output('qbit-0', 'control out', qBitSocket, false);
        var xIn = new Rete.Input('qbit-1', 'X in', qBitSocket, false);
        var xOut = new Rete.Output('qbit-1', 'X out', qBitSocket, false);
        this.addInput(contIn);
        this.addInput(xIn);
        this.addOutput(contOut);
        this.addOutput(xOut);
    }
}

class Measure extends Rete.Node {
    constructor() {
        super('Measure');
        var qin = new Rete.Input('qbit', 'qbit', qBitSocket, false);
        var cout = new Rete.Output('cbit', 'cbit', cBitSocket, false);
        this.addInput(qin);
        this.addOutput(cout);
    }
}

class CircuitOutput extends Rete.Node {
    constructor(cbits) {
        super('Circuit Output');
        for (var i = 0; i < cbits; i++) {
            var cin = new Rete.Input('cbit' + i, 'cbit-' + i, cBitSocket, false);
            this.addInput(cin);
        }
    }
}

(async () => {
    var container = document.querySelector('#rete');
    var circuitDisplay = document.querySelector('#circuitDiagram');

    var editor = new Rete.NodeEditor('qnd@0.1.0', container);
    editor.use(ConnectionPlugin.default);
    editor.use(ConnectionReroutePlugin.default);
    editor.use(VueRenderPlugin.default);
    editor.use(AreaPlugin);
    editor.use(KeyboardPlugin);

    [
        new QuantumCircuit(),
        new HadamardGate(),
        new ControlledX(),
        new Measure(),
        new CircuitOutput(),
    ].map(n => editor.register(n));

    var qc = new QuantumCircuit(2);
    var h = new HadamardGate();
    var cx = new ControlledX();
    var m1 = new Measure();
    var m2 = new Measure();
    var co = new CircuitOutput(2);
    h.position = [250, -50];
    cx.position = [525, 35];
    m1.position = [825, 30];
    m2.position = [825, 170];
    co.position = [1100, 100];
    editor.addNode(qc);
    editor.addNode(h);
    editor.addNode(cx);
    editor.addNode(m1);
    editor.addNode(m2);
    editor.addNode(co);
    editor.connect(qc.outputs.get('qbit1'), cx.inputs.get('qbit-1'));
    editor.connect(qc.outputs.get('qbit0'), h.inputs.get('qbit'));
    editor.connect(h.outputs.get('qbit'), cx.inputs.get('qbit-0'));
    editor.connect(cx.outputs.get('qbit-0'), m1.inputs.get('qbit'));
    editor.connect(cx.outputs.get('qbit-1'), m2.inputs.get('qbit'));
    editor.connect(m1.outputs.get('cbit'), co.inputs.get('cbit0'));
    editor.connect(m2.outputs.get('cbit'), co.inputs.get('cbit1'));

    // Update circuit on backend whenever there is a change
    editor.on('process nodecreated noderemoved connectioncreated connectionremoved', async () => {
        var json = JSON.stringify(editor.toJSON());
        var form = new FormData();
        form.append('node_json', json);
        var response = await fetch('create', {
            method: 'POST',
            body: form
        });
        response = await response.json();
        circuitDisplay.innerText = response['circuit'];
    });

    editor.view.resize();
    AreaPlugin.zoomAt(editor);
    editor.trigger('process');

    document.getElementById('reCenter').onclick = () => {
        AreaPlugin.zoomAt(editor, editor.nodes);
    };
})();