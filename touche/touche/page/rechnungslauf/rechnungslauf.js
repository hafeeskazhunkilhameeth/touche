frappe.pages['rechnungslauf'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Rechnungslauf',
		single_column: true
	});
	
	frappe.rechnungslauf.make(page);
	frappe.rechnungslauf.run(page);
	
	// add the application reference
	frappe.breadcrumbs.add("Touche");
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
	if (document.getElementById("mitglied-typ").classList.contains('hidden')) {
		document.getElementById("mitglied-typ").classList.remove('hidden');
	}
	/* if (document.getElementById("end").classList.contains('hidden')) {
		document.getElementById("end").classList.remove('hidden');
	} */
	if (document.getElementById("mitglied-typ-label").classList.contains('hidden')) {
		document.getElementById("mitglied-typ-label").classList.remove('hidden');
	}
	/* if (document.getElementById("end-label").classList.contains('hidden')) {
		document.getElementById("end-label").classList.remove('hidden');
	} */
}

function showPartialMitgliedDetails() {
	if (!document.getElementById("mitglied-typ").classList.contains('hidden')) {
		document.getElementById("mitglied-typ").classList.add('hidden');
	}
	if (!document.getElementById("mitglied-typ-label").classList.contains('hidden')) {
		document.getElementById("mitglied-typ-label").classList.add('hidden');
	}
	/* if (document.getElementById("end").classList.contains('hidden')) {
		document.getElementById("end").classList.remove('hidden');
	}
	if (document.getElementById("end-label").classList.contains('hidden')) {
		document.getElementById("end-label").classList.remove('hidden');
	} */
}

function hideMitgliedDetails() {
	if (!document.getElementById("mitglied-typ").classList.contains('hidden')) {
		document.getElementById("mitglied-typ").classList.add('hidden');
	}
	/* if (!document.getElementById("end").classList.contains('hidden')) {
		document.getElementById("end").classList.add('hidden');
	} */
	if (!document.getElementById("mitglied-typ-label").classList.contains('hidden')) {
		document.getElementById("mitglied-typ-label").classList.add('hidden');
	}
	/* if (!document.getElementById("end-label").classList.contains('hidden')) {
		document.getElementById("end-label").classList.add('hidden');
	} */
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
		lauf = "Anwalte";
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
			if (lauf == "Alle") {
				rechnungslaufAlle(lauf, end);
			} else if (lauf == "Mitglieder") {
				rechnungslaufMitglieder(lauf, end, mitglied_typ);
			} else if (lauf == "Anwalte") {
				rechnungslaufAnwalt(lauf);
			} else if (lauf == "Kanzleien") {
				rechnungslaufKanzlei(lauf);
			}
			return false;
		},
		function(){
			return false;
		}
	)
}

function rechnungslaufAlle(lauf, end) {
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
				if (document.getElementById("myTable").classList.contains('hidden')) {
					document.getElementById("myTable").classList.remove('hidden');
				}
				//console.log(r.message);
				for (y = 0; y < r.message.length; y++) {
					for (i = 0; i < r.message[y].length; i++) {
						var table = document.getElementById("myTable");
						var row = document.createElement("tr");
						var cell_1 = document.createElement("td");
						var cell_1_txt = document.createTextNode(String(y) + "." + String(i + 1));
						cell_1.appendChild(cell_1_txt);
						var cell_2 = document.createElement("td");
						var cell_2_txt = document.createTextNode(r.message[y][i]);
						cell_2.appendChild(cell_2_txt);
						row.appendChild(cell_1);
						row.appendChild(cell_2);
						table.appendChild(row);
					}
				}
			} else {
				closeNav();
				frappe.msgprint('Es wurde nichts gefunden, das den Kriterien entspricht.', 'Kein Output');
			}
		}
	});
}

function rechnungslaufMitglieder(lauf, end, mitglied_typ) {
	openNav();
	frappe.call({
		method: 'touche.touche.page.rechnungslauf.rechnungslauf.rechnungslauf',
		args: {
			'lauf': lauf,
			'end': end,
			'typ': mitglied_typ
		},
		callback: function(r) {
			if (r.message) {
				closeNav();
				//console.log(r.message);
				for (i = 0; i < r.message.length; i++) {
					var table = document.getElementById("myTable");
					var row = document.createElement("tr");
					var cell_1 = document.createElement("td");
					var cell_1_txt = document.createTextNode(i + 1);
					cell_1.appendChild(cell_1_txt);
					var cell_2 = document.createElement("td");
					var cell_2_txt = document.createTextNode(r.message[i]);
					cell_2.appendChild(cell_2_txt);
					row.appendChild(cell_1);
					row.appendChild(cell_2);
					table.appendChild(row);
				}
			} else {
				closeNav();
				frappe.msgprint('Es wurde nichts gefunden, das den Kriterien entspricht.', 'Kein Output');
			}
		}
	});
}

function rechnungslaufAnwalt(lauf) {
	openNav();
	frappe.call({
		method: 'touche.touche.page.rechnungslauf.rechnungslauf.rechnungslauf',
		args: {
			'lauf': lauf
		},
		callback: function(r) {
			if (r.message) {
				closeNav();
				//console.log(r.message);
				for (i = 0; i < r.message.length; i++) {
					var table = document.getElementById("myTable");
					var row = document.createElement("tr");
					var cell_1 = document.createElement("td");
					var cell_1_txt = document.createTextNode(i + 1);
					cell_1.appendChild(cell_1_txt);
					var cell_2 = document.createElement("td");
					var cell_2_txt = document.createTextNode(r.message[i]);
					cell_2.appendChild(cell_2_txt);
					row.appendChild(cell_1);
					row.appendChild(cell_2);
					table.appendChild(row);
				}
			} else {
				closeNav();
				frappe.msgprint('Es wurde nichts gefunden, das den Kriterien entspricht.', 'Kein Output');
			}
		}
	});
}

function rechnungslaufKanzlei(lauf) {
	openNav();
	frappe.call({
		method: 'touche.touche.page.rechnungslauf.rechnungslauf.rechnungslauf',
		args: {
			'lauf': lauf
		},
		callback: function(r) {
			if (r.message) {
				closeNav();
				//console.log(r.message);
				for (i = 0; i < r.message.length; i++) {
					var table = document.getElementById("myTable");
					var row = document.createElement("tr");
					var cell_1 = document.createElement("td");
					var cell_1_txt = document.createTextNode(i + 1);
					cell_1.appendChild(cell_1_txt);
					var cell_2 = document.createElement("td");
					var cell_2_txt = document.createTextNode(r.message[i]);
					cell_2.appendChild(cell_2_txt);
					row.appendChild(cell_1);
					row.appendChild(cell_2);
					table.appendChild(row);
				}
			} else {
				closeNav();
				frappe.msgprint('Es wurde nichts gefunden, das den Kriterien entspricht.', 'Kein Output');
			}
		}
	});
}

/* Open */
function openNav() {
    document.getElementById("myNav").style.display = "block";
}

/* Close */
function closeNav() {
    document.getElementById("myNav").style.display = "none";
}