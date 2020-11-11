var toolbox = document.getElementById('toolbox');

var grid = {
    spacing: 40,
    length: 2,
    color: '#000',
    snap: true
};

var move = {
    scrollbars: true,
    drag: true,
    wheel: true
};

var blocklyArea = document.getElementById('blocklyArea');
var workspace = Blockly.inject(blocklyArea, {
    toolbox: toolbox,
    grid: grid,
    sounds: false,
    move: move
});

var outputCode = document.getElementById('outputCode');

function blocks_updated() {
    var code = Blockly.Python.workspaceToCode(workspace);
    code = 'from qiskit import *\n\n' + code;
    outputCode.innerText = code;
    hljs.highlightBlock(outputCode);
    return code;
}
workspace.addChangeListener(blocks_updated);

function execute_code() {
    var req = new XMLHttpRequest();
    req.open('POST', '/projects/quantum_blocks/submit_code');
    req.onload = function () {
        if (req.status === 200) {
            alert(req.responseText);
        } else alert(req.responseText);
    };

    var form = new FormData();
    form.append('code', blocks_updated());
    req.send(form);
}
blocks_updated();