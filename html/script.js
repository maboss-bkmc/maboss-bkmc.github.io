
/*
  MaBoSS javascript file
  2012-03-23 Eric Viara
*/

function forall(id, action, hint) {
    var children = document.body.getElementsByTagName('*');
    for (var i = 0, length = children.length; i < length; i++) {
	child = children[i];
	if (child.id.substr(0, id.length) == id) {
	    if (action == 'hide') {
		child.style.display = 'none';
	    } else if (action == 'color') {
		child.style.color = hint;
	    } else if (action == 'fontWeight') {
		child.style.fontWeight = hint;
	    } /* else: ignoring */
	}
    }
}

function show(id) {
    forall('maboss_', 'hide', '')
    document.getElementById('maboss_'+id).style.display = 'block';
    var color = document.getElementById('mi_hidden').style.color;
    forall('mi_', 'color', color);
    forall('mi_', 'fontWeight', 'normal');
    document.getElementById('mi_'+id).style.fontWeight = 'bold';
}

function load_external(url, id) {
    fetch(url /*, options */)
    .then((response) => response.text())
    .then((html) => {
        document.getElementById(id).innerHTML = html;
    })
    .catch((error) => {
        console.warn(error);
    });
}

function load_externals () {
    load_external("UPMaBoSS/index.html", "maboss_upmaboss");
    load_external("EnsembleMaBoSS/index.html", "maboss_ensemblemaboss");
    load_external("pyMaBoSS/index.html", "maboss_pymaboss");
} 
