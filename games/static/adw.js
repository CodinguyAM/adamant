isturn = 0;
strthingy = "";

function upd() {
    inp = document.getElementById('code');
    localStorage.setItem("adage-username", inp.value);
    fetch('get-state-adw?c='.concat(inp.value)).then(resp => resp.json()).then(function(json) {
	tp = json.to_play;
	gs = json.guess;
	fb = json.fb;
	n = json.n;
	w = json.w;
	users = json.users;
	si = json.i;
	if (tp == si) {
		isturn = 1;
	}
	if (w >= 0) {
		
	} else {
		for (int i  = 0; i < n; i++) {
			row = document.getElementById(`wr_${i}`);
			if (i === tp) {
				row.className = 'adw-row adw-row-tp';
			} else if (i === si) {
				row.className = 'adw-row adw-row-s';
			} else {
				row.className = 'adw-row';
			}
			for (int j=0; j < n; j++) {
				el = document.getElementById(`subwordle_${i}_${j}`);
				innerhtml = "<table>";
				for (int k=0; k < gs[i][j].n; k++) {
					innerhtml += "<tr>"
					for (int l=0; l<5; l++) {
						if (fb[i][j].f[k][l] == '@') {
							innerhtml += `<td class='adw-green'>${gs[i][j].g[k][l]}</td>`;
						} else if (fb[i][j].f[k][l] == '+') {
							innerhtml += `<td class='adw-yellow'${gs[i][j].g[k][l]}</td>)`; 
						} else {
							innerhtml += `<td class='adw-grey'${gs[i][j].g[k][l]</td>}`;	
						}
					}
					innerhtml += "</tr>";
				}
				innerhtml += "</table>";
				el.innerHTML = innerhtml;
			}
		}
	}			
    });
};

document.addEventListener("keyup", 
	function (e) {
		kp = e.key;
		if ('QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm'.includes(kp)) {
			