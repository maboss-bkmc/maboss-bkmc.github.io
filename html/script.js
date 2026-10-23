
/*
  MaBoSS javascript file
  2012-03-23 Eric Viara
*/

function forall(id, action) {
    var children = document.body.getElementsByTagName('*');
    for (var i = 0, length = children.length; i < length; i++) {
	var child = children[i];
	if (child.id.substr(0, id.length) == id) {
	    if (action == 'hide') {
		child.style.display = 'none';
	    } else if (action == 'deactivate') {
		child.classList.remove('active');
	    } /* else: ignoring */
	}
    }
}

function show(id) {
    forall('maboss_', 'hide');
    document.getElementById('maboss_'+id).style.display = 'block';
    forall('mi_', 'deactivate');
    document.getElementById('mi_'+id).classList.add('active');
    set_menu_open(false);
    window.scrollTo(0, 0);
    // Keep the current page in the URL, so that it can be linked to
    history.replaceState(null, '', id == 'home' ? location.pathname : '#' + id);
}

function set_menu_open(open) {
    document.getElementById('menu').classList.toggle('menu_open', open);
    document.getElementById('menu_toggle').setAttribute('aria-expanded', open ? 'true' : 'false');
}

function toggle_menu() {
    set_menu_open(!document.getElementById('menu').classList.contains('menu_open'));
}

function show_from_hash() {
    var id = location.hash.substr(1);
    if (id && document.getElementById('maboss_' + id) && document.getElementById('mi_' + id)) {
        show(id);
    }
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
    load_external("EnsembleMaBoSS/index.html", "maboss_ensemblemaboss");
} 

function show_tab(group, name) {
    var tabs = document.getElementsByClassName('tab');
    for (var i = 0; i < tabs.length; i++) {
	if (tabs[i].id.substr(0, group.length + 5) == group + '_tab_') {
	    tabs[i].classList.toggle('tab_active', tabs[i].id == group + '_tab_' + name);
	}
    }
    var panels = document.getElementsByClassName('tab_panel');
    for (var i = 0; i < panels.length; i++) {
	if (panels[i].id.substr(0, group.length + 7) == group + '_panel_') {
	    panels[i].classList.toggle('hidden_panel', panels[i].id != group + '_panel_' + name);
	}
    }
}
