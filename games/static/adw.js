isturn = 0;
strthingy = "";

function upd() {
    inp = document.getElementById('code');
    fetch('get-state-adw?c='.concat(inp.value)).then(resp => resp.json()).then(function(json) {
	console.log(json);
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
		location.reload()
	} else {
		for (let i = 0; i < n; i++) {
			wsp = document.getElementById(`wsp_${i}`);
			gsp = document.getElementById(`gsp_${i}`);
			wsp.innerHTML = users[i];
			gsp.innerHTML = users[i];
			row = document.getElementById(`wr_${i}`);
			gh = document.getElementById(`wgh_${i}`);
			if (i === tp) {
				row.className = 'adw-row adw-row-tp';
				gh.className = 'guess-header guess-header-tp';
			} else if (i === si) {
				row.className = 'adw-row adw-row-s';
				gh.className = 'guess-header guess-header-s';
			} else {
				row.className = 'adw-row';
				gh.className = 'guess-header';
			}
			for (let j=0; j < n; j++) {
				el = document.getElementById(`sw_${i}_${j}`);
				innerhtml = "<table>";
				for (let k=0; k < gs[i].length; k++) {
					innerhtml += "<tr>"
					for (let l=0; l<5; l++) {
						if (fb[i][j][k][l] == '@') {
							innerhtml += `<td><div class='adw-green'>${gs[i][k][l].toUpperCase()}</div></td>`;
						} else if (fb[i][j][k][l] == '+') {
							innerhtml += `<td><div class='adw-yellow'>${gs[i][k][l].toUpperCase()}</div></td>`; 
						} else {
							innerhtml += `<td><div class='adw-grey'>${gs[i][k][l].toUpperCase()}</div></td>`;	
						}
					}
					innerhtml += "</tr>";
				}
				if (isturn && i == si) {
					innerhtml += "<tr>";
					for (let m=0; m<5; m++) {
						innerhtml += `<td><div class='adw-empty adw-input-${m}'></div></td>`;
					}
					innerhtml += "</tr>";
				}
				innerhtml += "</table>";
				console.log(innerhtml);
				el.innerHTML = innerhtml;
			}
		}
	}

	for (let stri=0; stri<strthingy.length; stri++) {
		classname = `adw-input-${stri}`;
		tbs = document.getElementsByClassName(classname);
		for (const tb of tbs) {
			tb.innerText = strthingy[stri].toUpperCase();
		}
	}			
    });
};

document.addEventListener("keyup", 
	function (e) {
		kp = e.key;
		if ('QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm'.includes(kp) && strthingy.length < 5 && isturn==1) {
			kp = kp.toLowerCase();			
			strthingy += kp;
		} else if (kp === "Enter") {
			cmwt = document.csrfmiddlewaretoken
			c = cmwt.innerText;
			fetch(window.location.href, {
				method: "POST",
				headers: {'Content-Type': 'application/json'},
				body: JSON.stringify({
					csrfmiddlewaretoken: c,
					code: inp.value,
					guess: strthingy,
				})
			}).then(resp => resp.json()).then(function(json) {
				if (!json.accepted) {
					alert(json.msg);
				}
			});
			delay(100);
			strthingy = "";
		} else if ((kp === "Backspace" || kp === "Delete") && strthingy.length > 0) {
			strthingy = strthingy.slice(0, strthingy.length-1);
			classname = `adw-input-${strthingy.length}`;
		}
	})

document.addEventListener("DOMContentLoaded",
	function (e) {
		setInterval(upd, 20);
	})