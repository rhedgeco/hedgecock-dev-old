const qBitSocket = new Rete.Socket('Quantum Bit');
const cBitSocket = new Rete.Socket('Classical Bit');

class QuantumCircuit extends Rete.Node {
    constructor(qbits) {
        super('Quantum Circuit');
        for (let i = 0; i < qbits; i++) {
            let qout = new Rete.Output('qbit' + i, 'QBit-' + i, qBitSocket, false);
            this.addOutput(qout);
        }
    }
}

class QuantumMeasure extends Rete.Node {
    constructor(qbits) {
        super('Measure Circuit');
        for (let i = 0; i < qbits; i++) {
            let qin = new Rete.Input('cbit' + i, 'CBit-' + i, qBitSocket, false);
            this.addInput(qin);
        }
    }
}

(async () => {
    var container = document.querySelector('#rete');

    var editor = new Rete.NodeEditor('qnd@0.1.0', container);
    editor.use(ConnectionPlugin.default);
    editor.use(VueRenderPlugin.default);
    editor.use(AreaPlugin);

    var qc = new QuantumCircuit(2);
    var qm = new QuantumMeasure(2);
    qm.position = [500, 100];
    editor.register(qc);
    editor.addNode(qc);
    editor.register(qm);
    editor.addNode(qm);
    editor.connect(qc.outputs.get('qbit0'), qm.inputs.get('cbit0'));
    editor.connect(qc.outputs.get('qbit1'), qm.inputs.get('cbit1'));

    editor.view.resize();
    editor.trigger('process');
    AreaPlugin.zoomAt(editor);

    document.getElementById('reCenter').onclick = () => {
        AreaPlugin.zoomAt(editor, editor.nodes);
    };
})();