document.addEventListener('DOMContentLoaded', function() {
    form = document.getElementById('loginform');
    inp = document.getElementById('username-inp');
    form.onsubmit = function() {
        localStorage.setItem("adage-username", inp.value);
	fetch('get-settings?u='.concat(inp.value)).then(resp => resp.json()).then(function(json) {
	    localStorage.setItem('adage-primary', json.primary);
	    localStorage.setItem('adage-secondary', json.secondary);
	    localStorage.setItem('adage-tertiary', json.tertiary);
	    localStorage.setItem('adage-quaternary', json.quaternary);
	    localStorage.setItem('adage-faint1', json.faint1);
	    localStorage.setItem('adage-faint2', json.faint2);
	    localStorage.setItem('adage-sfaint1', json.sfaint1);
	    localStorage.setItem('adage-sfaint2', json.sfaint2);
	    localStorage.setItem('adage-bgcolor', json.bgcolor);
	    localStorage.setItem('adage-affirm', json.affirm);
	    localStorage.setItem('adage-affirm2', json.affirm2);
	    localStorage.setItem('adage-neutral', json.neutral);
	    localStorage.setItem('adage-negative', json.negative);
	    localStorage.setItem('adage-font-family', json.font_family);
	    localStorage.setItem('adage-font-heading', json.font_heading);
	});

    };
})