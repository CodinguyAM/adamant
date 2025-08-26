document.addEventListener('DOMContentLoaded', function() {
    if (localStorage.getItem('adage-faint1')) {
        var ds = document.getElementById('defaultstyle');
        ds.innerHTML = `
        body {
            background-color: ${localStorage.getItem('adage-bgcolor')};
            font-family: ${localStorage.getItem('adage-font-family')};
	    margin-top: 5px;
	    margin-bottom: 5px;
        }

        .navel {
            background-color: ${localStorage.getItem('adage-faint1')};
            border-radius: 10px;
            display: inline-block;
            margin: auto;
            margin-top: 5px;
            margin-bottom: 5px;
            padding: 2px;
        }

        h1, h2, h3, h4, h5, h6 {
            font-family: ${localStorage.getItem('adage-font-heading')}
        }

	h1 {
	    text-align: center;
	}

        nav {
            display: flex;
            justify-content: space-evenly;
            background-color: ${localStorage.getItem('adage-sfaint1')};
        }

	.prim-el {
	    background-color: ${localStorage.getItem('adage-primary')};
	    border-color: ${localStorage.getItem('adage-primary')};

	}

	.w40 {
	    width: 40%;
	    margin: auto;
	}

	#logospan {
	    color: #5CD444;
	}

	btn-primary {
	    margin-top: 5px;
	    margin-bottom: 5px;
	}

        `

	var sv = document.getElementById('stylevars');
	sv.innerHTML = `
	:root {
		--adage-primary: ${localStorage.getItem('adage-primary')};
		--adage-secondary: ${localStorage.getItem('adage-secondary')};
		--adage-tertiary: ${localStorage.getItem('adage-tertiary')};
		--adage-quaternary: ${localStorage.getItem('adage-quaternary')};
		--adage-faint-p: ${localStorage.getItem('adage-faint1')};
		--adage-faint-s: ${localStorage.getItem('adage-faint2')};
		--adage-fainter-p: ${localStorage.getItem('adage-sfaint1')};
		--adage-fainter-s: ${localStorage.getItem('adage-sfaint2')};
		--adage-background-color: ${localStorage.getItem('adage-bgcolor')};
		--adage-affirm: ${localStorage.getItem('adage-affirm')};
		--adage-affirm-s: ${localStorage.getItem('adage-affirm2')};
		--adage-neutral: ${localStorage.getItem('adage-neutral')};
		--adage-negative: ${localStorage.getItem('adage-negative')};
		--adage-font-body: ${localStorage.getItem('adage-font-family')};
		--adage-font-heading: ${localStorage.getItem('adage-font-heading')};
		--adage-highlight-background-color: ${localStorage.getItem('adage-fbgcolor')};
	}
	`	
		

    } else {
        var ds = document.getElementById('defaultstyle');
        ds.innerHTML = `
        body {
            background-color: #FFFFFF;
            font-family: Helvetica;
	    margin-top: 5px;
	    margin-bottom: 5px;
        }

        .navel {
            background-color: #ABCDEF;
            border-radius: 10px;
            display: inline-block;
            margin: auto;
            margin-top: 5px;
            margin-bottom: 5px;
            padding: 2px;
        }

        h1, h2, h3, h4, h5, h6 {
            font-family: Helvetica;
        }
	
	h1 {
	    text-align: center;
	}

        nav {
            display: flex;
            justify-content: space-evenly;
            background-color: #D5E6F7;
        }

	.prim-el {
	    background-color: #03A5FC;
	    border-color: #03A5FC;
	}
	.w40 {
	    width: 40%;
	    margin: auto;
	}

	#logospan {
	    color: #5CD444;
	}

	btn-primary {
	    margin-top: 5px;
	    margin-bottom: 5px;
	}
        `

	var sv = document.getElementById('stylevars');
	sv.innerHTML = `
	:root {
		--adage-primary: #03A5FC;
		--adage-secondary: #FC0B03;
		--adage-tertiary: #FAD102;
		--adage-quaternary: #02FABC;
		--adage-faint-p: #ABCDEF;
		--adage-faint-s: #D6C1C1;
		--adage-fainter-p: #D5E6F7;
		--adage-fainter-s: #EBE0E0;
		--adage-background-color: #FFFFFF;
		--adage-affirm: #639919;
		--adage-affirm-s: #F5E911;
		--adage-neutral: #777777;
		--adage-negative: #C94040;
		--adage-font-body: Helvetica;
		--adage-font-heading: Helvetica;
	}
	`

    }
    logout_btn = document.getElementById('logout-btn'); // I know it isn't an actual button, but it's styled to look like one.
    if (logout_btn != null) {
        logout_btn.onclick = function () {
            localStorage.removeItem("adage-username");
    	    localStorage.removeItem('adage-primary');
	    localStorage.removeItem('adage-secondary');
	    localStorage.removeItem('adage-tertiary');
	    localStorage.removeItem('adage-quaternary');
	    localStorage.removeItem('adage-faint1');
	    localStorage.removeItem('adage-faint2');
	    localStorage.removeItem('adage-sfaint1');
	    localStorage.removeItem('adage-sfaint2');
	    localStorage.removeItem('adage-bgcolor');
	    localStorage.removeItem('adage-affirm');
	    localStorage.removeItem('adage-affirm2');
	    localStorage.removeItem('adage-neutral');
	    localStorage.removeItem('adage-negative');
	    localStorage.removeItem('adage-font-family');
	    localStorage.removeItem('adage-font-heading');
        };
    }
})