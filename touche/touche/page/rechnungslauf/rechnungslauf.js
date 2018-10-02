frappe.pages['rechnungslauf'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Rechnungslauf',
		single_column: true
	});
	
	frappe.rechnungslauf.make(page);
	frappe.rechnungslauf.run(page);
	
	// add the application reference
	frappe.breadcrumbs.add("Pflanzenfreund");
}

frappe.rechnungslauf = {
	start: 0,
	make: function(page) {
		var me = frappe.rechnungslauf;
		me.page = page;
		me.body = $('<div></div>').appendTo(me.page.main);
		var data = "";
		$(frappe.render_template('rechnungslauf', data)).appendTo(me.body);
		

	},
	run: function(page) {
 
	}
}

function showMitgliedDetails() {
	document.getElementById("mitglied-typ").classList.remove('hidden');
	document.getElementById("end").classList.remove('hidden');
	document.getElementById("mitglied-typ-label").classList.remove('hidden');
	document.getElementById("end-label").classList.remove('hidden');
}

function hideMitgliedDetails() {
	document.getElementById("mitglied-typ").classList.add('hidden');
	document.getElementById("end").classList.add('hidden');
	document.getElementById("mitglied-typ-label").classList.add('hidden');
	document.getElementById("end-label").classList.add('hidden');
}

function startRechnungslauf() {
	var lauf = "";
	var mitglied_typ = document.getElementById("mitglied-typ").value;
	var end = document.getElementById("end").value;
	var confirmText = "";
	
	if (document.getElementById('alle').checked) {
		lauf = "Alle";
	} else if (document.getElementById('mitglieder').checked) {
		lauf = "Mitglieder";
	} else if (document.getElementById('anwalt').checked) {
		lauf = "Anwälte";
	} else if (document.getElementById('kanzlei').checked) {
		lauf = "Kanzleien";
	}
	
	if ((lauf == "Alle") || (lauf == "Mitglieder")) {
		confirmText = "Sie haben folgende Auswahl getroffen, möchten Sie den Rechnungslauf starten?<br><b>Rechnungslauf für: </b> " + lauf +
			"<br><b>Mitglied Typ: </b> " + mitglied_typ +
			"<br><b>Mitglied bis: </b> " + end;
	} else {
		confirmText = "Sie haben folgende Auswahl getroffen, möchten Sie den Rechnungslauf starten?<br><b>Rechnungslauf für: </b> " + lauf;
	}
	frappe.confirm(
		confirmText,
		function(){
			console.log(lauf + " / " + mitglied_typ + " / " + end);
			if (lauf == "Alle") {
				rechnungslaufAlle(lauf, end);
			} else if (lauf == "Mitglieder") {
				rechnungslaufMitglieder();
			} else if (lauf == "Anwälte") {
				rechnungslaufAnwalt();
			} else if (lauf == "Kanzleien") {
				rechnungslaufKanzlei();
			}
			return false;
		},
		function(){
			return false;
		}
	)
}

function rechnungslaufAlle(lauf, end) {
	console.log("go alle");
	openNav();
	frappe.call({
		method: 'touche.touche.page.rechnungslauf.rechnungslauf.rechnungslauf',
		args: {
			'lauf': lauf,
			'end': end
		},
		callback: function(r) {
			if (r.message) {
				closeNav();
				console.log(r.message);
			} else {
				closeNav();
				frappe.msgprint('Es wurde nichts gefunden, das den Kriterien entspricht.', 'Kein Output');
			}
		}
	});
}

function rechnungslaufMitglieder() {
	console.log("go mitglieder");
	openNav();
}

function rechnungslaufAnwalt() {
	console.log("go anwalt");
	openNav();
}

function rechnungslaufKanzlei() {
	console.log("go kanzlei");
	openNav();
}

/* Open */
function openNav() {
    document.getElementById("myNav").style.display = "block";
}

/* Close */
function closeNav() {
    document.getElementById("myNav").style.display = "none";
}