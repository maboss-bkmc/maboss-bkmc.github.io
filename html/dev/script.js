
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
