const qBitSocket = new Rete.Socket('Quantum Bit');
const cBitSocket = new Rete.Socket('Classical Bit');

class QuantumCircuit extends Rete.Node {
    constructor(qbits) {
        super('Quantum Circuit');
        for (let i = 0; i < qbits; i++) {
            let qout = new Rete.Output('qbit' + i, 'Quantum-' + i, qBitSocket, false);
            this.addOutput(qout);
        }
    }
}

class Measure extends Rete.Node {
    constructor() {
        super('Measure');
        let qin = new Rete.Input('qbit', 'Quantum', qBitSocket, false);
        let cout = new Rete.Output('cbit', 'Classic', cBitSocket, false);
        this.addInput(qin);
        this.addOutput(cout);
    }
}

class CircuitOutput extends Rete.Node {
    constructor(cbits) {
        super('Circuit Output');
        for (let i = 0; i < cbits; i++) {
            let cin = new Rete.Input('cbit' + i, 'Classic-' + i, cBitSocket, false);
            this.addInput(cin);
        }
    }
}

(async () => {
    var container = document.querySelector('#rete');

    var editor = new Rete.NodeEditor('qnd@0.1.0', container);
    editor.use(ConnectionPlugin.default);
    editor.use(ConnectionReroutePlugin.default);
    editor.use(VueRenderPlugin.default);
    editor.use(AreaPlugin);

    var qc = new QuantumCircuit(2);
    var m1 = new Measure();
    var m2 = new Measure();
    var co = new CircuitOutput(2);
    m1.position = [350, 30];
    m2.position = [350, 170];
    co.position = [700, 200];
    editor.register(qc);
    editor.register(m1);
    editor.register(co);
    editor.addNode(qc);
    editor.addNode(m1);
    editor.addNode(m2);
    editor.addNode(co);
    editor.connect(qc.outputs.get('qbit0'), m1.inputs.get('qbit'));
    editor.connect(qc.outputs.get('qbit1'), m2.inputs.get('qbit'));
    editor.connect(m1.outputs.get('cbit'), co.inputs.get('cbit0'));
    editor.connect(m2.outputs.get('cbit'), co.inputs.get('cbit1'));

    editor.on('process nodecreated noderemoved connectioncreated connectionremoved', async () => {
        var json = JSON.stringify(editor.toJSON());
    });

    editor.view.resize();
    AreaPlugin.zoomAt(editor);

    document.getElementById('reCenter').onclick = () => {
        AreaPlugin.zoomAt(editor, editor.nodes);
    };
})();