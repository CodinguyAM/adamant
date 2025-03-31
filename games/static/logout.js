document.addEventListener('DOMContentLoaded', function() {
    form = document.getElementById('loginform');
    form.onsubmit = function() {
        localStorage.removeItem("adage-username");
	localStorage.removeItem('adage-primary');
	localStorage.removeItem('adage-secondary');
	localStorage.removeItem('adage-tertiary';
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
})