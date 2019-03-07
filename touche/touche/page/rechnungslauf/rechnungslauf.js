frappe.pages['rechnungslauf'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Rechnungslauf',
		single_column: true
	});
	
	frappe.rechnungslauf.make(page);
	frappe.rechnungslauf.run(page);
	page.job_content = $(page.body).find('#placeForWorkers');
	
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

frappe.realtime.on("invoice_progress", function(data) {
	if (data.progress) {
		//console.log(data.progress);
		let progress_bar = document.getElementById("rechnungsprogress");
			if (progress_bar) {
				$(progress_bar).removeClass("progress-bar-danger").addClass("progress-bar-success progress-bar-striped");
				$(progress_bar).css("width", data.progress+"%");
			}
	}
});
frappe.realtime.on("invoices", function(data) {
	if (data.invoices) {
		clearTable();
		if (document.getElementById("myTable").classList.contains('hidden')) {
			document.getElementById("myTable").classList.remove('hidden');
		}

		var invoices = data.invoices;
		//console.log(invoices);
		for (y = 0; y < invoices.length; y++) {
			var pos = String(y + 1);
			var referenz = invoices[y][0];
			var mitglied_art = invoices[y][1];
			var betrag = invoices[y][2];
			crateTableContentElement(pos, referenz, mitglied_art, betrag);
		}
		document.getElementById("start_btn").classList.add("hidden");
		document.getElementById("pdf_btn").classList.remove("hidden");
	} else {
		let progress_bar = document.getElementById("rechnungsprogress");
			if (progress_bar) {
				$(progress_bar).removeClass("progress-bar-danger").addClass("progress-bar-success progress-bar-striped");
				$(progress_bar).css("width", data.progress+"%");
			}
		frappe.msgprint("Es wurden keine Rechnungen erstellt");
	}
});
frappe.realtime.on("pdf_progress", function(data) {
	if (data.progress) {
		//console.log(data.progress);
		let progress_bar = document.getElementById("rechnungsprogress");
			if (progress_bar) {
				$(progress_bar).removeClass("progress-bar-danger").addClass("progress-bar-success progress-bar-striped");
				$(progress_bar).css("width", data.progress+"%");
			}
		frappe.pages.rechnungslauf.refresh_jobs();
	}
});
frappe.realtime.on("print_progress", function(data) {
	if (data.progress) {
		//console.log(data.progress);
		let progress_bar = document.getElementById("printprogress");
			if (progress_bar) {
				$(progress_bar).parent().removeClass("hidden");
				$(progress_bar).addClass("progress-bar-success progress-bar-striped");
				$(progress_bar).css("width", data.progress+"%");
			}
	}
});

/* frappe.pages['rechnungslauf'].on_page_show = function(wrapper) {
	
} */

frappe.pages.rechnungslauf.refresh_jobs = function() {
	var page = frappe.pages.rechnungslauf.page;

	// don't call if already waiting for a response
	if(page.called) return;
	page.called = true;
	frappe.call({
		method: 'touche.touche.page.rechnungslauf.rechnungslauf.list_all_pdfs',
		callback: function(r) {
			page.called = false;
			page.body.find('.list-jobs').remove();
			$(frappe.render_template('background_jobs', {onlyfiles:r.message || []})).appendTo(page.job_content);

			if(frappe.get_route()[0]==='rechnungslauf') {
				frappe.background_jobs_timeout = setTimeout(frappe.pages.rechnungslauf.refresh_jobs, 2000);
			}
		}
	});
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
	
	if (document.getElementById('mitglieder').checked) {
		lauf = "Mitglieder";
	} else if (document.getElementById('anwalt').checked) {
		lauf = "Anwalte";
	} else if (document.getElementById('kanzlei').checked) {
		lauf = "Kanzleien";
	}
	
	if (lauf == "Mitglieder") {
		confirmText = "Sie haben folgende Auswahl getroffen, möchten Sie den Rechnungslauf starten?<br><b>Rechnungslauf für: </b> " + lauf +
			"<br><b>Mitglied Typ: </b> " + mitglied_typ;
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
	//openNav();
	frappe.call({
		method: 'touche.touche.page.rechnungslauf.rechnungslauf.rechnungslauf',
		args: {
			'lauf': lauf,
			'end': end
		},
		callback: function(r) {
			/* if (r.message) {
				closeNav();
				/* clearTable();
				if (document.getElementById("myTable").classList.contains('hidden')) {
					document.getElementById("myTable").classList.remove('hidden');
				}
				//console.log(r.message);
				for (y = 0; y < r.message.length; y++) {
					for (i = 0; i < r.message[y].length; i++) {
						var pos = String(y + 1) + "." + String(i + 1);
						var referenz = r.message[y][i][0];
						var mitglied_art = r.message[y][i][1];
						var betrag = r.message[y][i][2];
						crateTableContentElement(pos, referenz, mitglied_art, betrag);
					}
				} 
			} else {
				closeNav();
				frappe.msgprint('Es wurde nichts gefunden, das den Kriterien entspricht.', 'Kein Output');
			} */
		}
	});
}

function rechnungslaufMitglieder(lauf, end, mitglied_typ) {
	//openNav();
	frappe.call({
		method: 'touche.touche.page.rechnungslauf.rechnungslauf.rechnungslauf',
		args: {
			'lauf': lauf,
			'end': end,
			'typ': mitglied_typ
		},
		callback: function(r) {
			/* if (r.message) {
				closeNav();
				clearTable();
				if (document.getElementById("myTable").classList.contains('hidden')) {
					document.getElementById("myTable").classList.remove('hidden');
				}
				//console.log(r.message);
				for (i = 0; i < r.message.length; i++) {
					var pos = i + 1;
					var referenz = r.message[i][0];
					var mitglied_art = r.message[i][1];
					var betrag = r.message[i][2];
					crateTableContentElement(pos, referenz, mitglied_art, betrag);
				}
			} else {
				closeNav();
				frappe.msgprint('Es wurde nichts gefunden, das den Kriterien entspricht.', 'Kein Output');
			} */
		}
	});
}

function rechnungslaufAnwalt(lauf) {
	//openNav();
	frappe.call({
		method: 'touche.touche.page.rechnungslauf.rechnungslauf.rechnungslauf',
		args: {
			'lauf': lauf
		},
		callback: function(r) {
			/* if (r.message) {
				closeNav();
				clearTable();
				if (document.getElementById("myTable").classList.contains('hidden')) {
					document.getElementById("myTable").classList.remove('hidden');
				}
				//console.log(r.message);
				for (i = 0; i < r.message.length; i++) {
					var pos = i + 1;
					var referenz = r.message[i][0];
					var mitglied_art = r.message[i][1];
					var betrag = r.message[i][2];
					crateTableContentElement(pos, referenz, mitglied_art, betrag);
				}
			} else {
				closeNav();
				frappe.msgprint('Es wurde nichts gefunden, das den Kriterien entspricht.', 'Kein Output');
			} */
		}
	});
}

function rechnungslaufKanzlei(lauf) {
	//openNav();
	frappe.call({
		method: 'touche.touche.page.rechnungslauf.rechnungslauf.rechnungslauf',
		args: {
			'lauf': lauf
		},
		callback: function(r) {
			/* if (r.message) {
				closeNav();
				clearTable();
				if (document.getElementById("myTable").classList.contains('hidden')) {
					document.getElementById("myTable").classList.remove('hidden');
				}
				//console.log(r.message);
				for (i = 0; i < r.message.length; i++) {
					var pos = i + 1;
					var referenz = r.message[i][0];
					var mitglied_art = r.message[i][1];
					var betrag = r.message[i][2];
					crateTableContentElement(pos, referenz, mitglied_art, betrag);
				}
			} else {
				closeNav();
				frappe.msgprint('Es wurde nichts gefunden, das den Kriterien entspricht.', 'Kein Output');
			} */
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

function clearTable() {
	var tabelle = document.getElementById("myTable");
	var rowCount = tabelle.rows.length;
	for (var i = rowCount - 1; i > 0; i--) {
		tabelle.deleteRow(i);
	}
}

function crateTableContentElement(pos, referenz, mitglied_art, betrag) {
	var table = document.getElementById("myTable");
	var row = document.createElement("tr");
	
	var cell_1 = document.createElement("td");
	var cell_1_txt = document.createTextNode(pos);
	cell_1.appendChild(cell_1_txt);
	
	var cell_2 = document.createElement("td");
	var cell_2_txt = document.createTextNode(referenz);
	cell_2.appendChild(cell_2_txt);
	
	var cell_3 = document.createElement("td");
	var cell_3_txt = document.createTextNode(mitglied_art);
	cell_3.appendChild(cell_3_txt);
	
	var cell_4 = document.createElement("td");
	var cell_4_txt = document.createTextNode(betrag);
	cell_4.appendChild(cell_4_txt);
	
	row.appendChild(cell_1);
	row.appendChild(cell_2);
	row.appendChild(cell_3);
	row.appendChild(cell_4);
	row.onclick = function() { 
		window.location = '/desk#Form/Sales Invoice/' + referenz
	};
	table.appendChild(row);
}

function createBindPDF() {
	var rechnungsdatum = frappe.datetime.get_today();
	frappe.confirm(
		"Wollen Sie ein Sammel-PDF aller gültigen Rechnungen mit dem Valuta-Datum " + rechnungsdatum + " erstellen?",
		function(){
			//frappe.msgprint("Der Job wurde dem Background-Worker übergeben.");
			startCreateBindPDF();
		},
		function(){
			return false;
		}
	)
}

function startCreateBindPDF() {
	frappe.call({
		method: 'touche.touche.page.rechnungslauf.rechnungslauf.createSammelPDF',
		args: {},
		callback: function(r) {}
	});
}

function deleteAllPDF() {
	frappe.confirm(
		"Wollen Sie alle oben aufgeführten PDF's vom Server entfernen?",
		function(){
			frappe.call({
				method: 'touche.touche.page.rechnungslauf.rechnungslauf.remove_downloaded_pdf',
				callback: function(r) {
					frappe.msgprint("Die PDF's wurden entfernt");
				}
			});
		},
		function(){
			return false;
		}
	)
}