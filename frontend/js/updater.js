function update_frontend() {
    var file = document.getElementById('file-upload').files[0];
    var form = new FormData();
    form.append('file', file);

    var req = new XMLHttpRequest();
    req.open('POST', '/api/update_frontend', true);
    req.onload = function (event) {
        if (req.status === 200) {
            alert('Updated!');
        } else {
            alert(req.responseText);
        }
    };
    req.send(form);
}