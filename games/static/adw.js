document.addEventListener('DOMContentLoaded', function() {
    inp = document.getElementById('code');
    localStorage.setItem("adage-username", inp.value);
    fetch('get-state-adw?c='.concat(inp.value)).then(resp => resp.json()).then(function(json) {
	tp = json.to_play;
	words = json.words;
	fb = json.fb;
	n = json.n;
	rows = document.getElementById
    });

    };
})