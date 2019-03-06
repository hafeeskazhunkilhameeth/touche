frappe.pages['touche-suchmaske'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Touche Suchmaske',
		single_column: true
	});
	
	frappe.touche_suchmaske.make(page);
	frappe.touche_suchmaske.run(page);
	
	// add the application reference
	frappe.breadcrumbs.add("Touche");
}

frappe.touche_suchmaske = {
	start: 0,
	make: function(page) {
		var me = frappe.touche_suchmaske;
		me.page = page;
		me.body = $('<div></div>').appendTo(me.page.main);
		var data = "";
		$(frappe.render_template('touche_suchmaske', data)).appendTo(me.body);
		

	},
	run: function(page) {
 
	}
}

function changeSuchtyp() {
	var typ = document.getElementById("suchtyp").value;
	if (typ == "Fachkontakte") {
		document.getElementById("load_btn").classList.remove("hidden");
		document.getElementById("fachkontaktfilter").classList.remove("hidden");
		document.getElementById("fachkontakttabelle").classList.remove("hidden");
		document.getElementById("kundenfilter").classList.add("hidden");
		document.getElementById("kundentabelle").classList.add("hidden");
		var tabelle = document.getElementById("myTableFK");

		var rowCount = tabelle.rows.length;
		for (var i = rowCount - 1; i > 0; i--) {
			tabelle.deleteRow(i);
		}
	}
	if (typ == "Kunden") {
		document.getElementById("load_btn").classList.remove("hidden");
		document.getElementById("fachkontaktfilter").classList.add("hidden");
		document.getElementById("fachkontakttabelle").classList.add("hidden");
		document.getElementById("kundenfilter").classList.remove("hidden");
		document.getElementById("kundentabelle").classList.remove("hidden");
		var tabelle = document.getElementById("myTable");

		var rowCount = tabelle.rows.length;
		for (var i = rowCount - 1; i > 0; i--) {
			tabelle.deleteRow(i);
		}
	}
	if (typ == "Bitte Suchtyp auswählen") {
		document.getElementById("load_btn").classList.add("hidden");
		document.getElementById("fachkontaktfilter").classList.add("hidden");
		document.getElementById("fachkontakttabelle").classList.add("hidden");
		document.getElementById("kundenfilter").classList.add("hidden");
		document.getElementById("kundentabelle").classList.add("hidden");
		var tabelle = document.getElementById("myTableFK");

		var rowCount = tabelle.rows.length;
		for (var i = rowCount - 1; i > 0; i--) {
			tabelle.deleteRow(i);
		}
		var _tabelle = document.getElementById("myTable");

		var _rowCount = _tabelle.rows.length;
		for (var i = _rowCount - 1; i > 0; i--) {
			_tabelle.deleteRow(i);
		}
	}
}

/* Open */
function openNav() {
    document.getElementById("myNav").style.display = "block";
}

/* Close */
function closeNav() {
    document.getElementById("myNav").style.display = "none";
}


//Suchfunktionen FK
function searchByFirstNameFK(searchID="FirstNameInputFK", searchIn="0") {
  // Declare variables
  var input, filter, table, tr, td, i;
  input = document.getElementById(searchID);
  filter = input.value.toUpperCase();
  table = document.getElementById("myTableFK");
  tr = table.getElementsByTagName("tr");

  // Loop through all table rows, and hide those who don't match the search query
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[parseInt(searchIn)];
    if (td) {
      if (td.innerHTML.toUpperCase().indexOf(filter) > -1) {
		tr[i].style.display = "";
		tr[i].classList.remove("FirstNameInputFK");
	  } else {
		tr[i].style.display = "none";
		tr[i].classList.add("FirstNameInputFK");
	  }
    }
  }
}
function searchByLastNameFK(searchID="LastNameInputFK", searchIn="1") {
  // Declare variables
  var input, filter, table, tr, td, i;
  input = document.getElementById(searchID);
  filter = input.value.toUpperCase();
  table = document.getElementById("myTableFK");
  tr = table.getElementsByTagName("tr");

  // Loop through all table rows, and hide those who don't match the search query
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[parseInt(searchIn)];
    if (td) {
      if (td.innerHTML.toUpperCase().indexOf(filter) > -1) {
		tr[i].style.display = "";
		tr[i].classList.remove("LastNameInputFK");
	  } else {
		tr[i].style.display = "none";
		tr[i].classList.add("LastNameInputFK");
	  }
    }
  }
}
function searchByTyp(searchID="typInput", searchIn="2") {
  // Declare variables
  var input, filter, table, tr, td, i;
  input = document.getElementById(searchID);
  filter = input.value.toUpperCase();
  table = document.getElementById("myTableFK");
  tr = table.getElementsByTagName("tr");

  // Loop through all table rows, and hide those who don't match the search query
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[parseInt(searchIn)];
    if (td) {
      if (td.innerHTML.toUpperCase().indexOf(filter) > -1) {
		tr[i].style.display = "";
		tr[i].classList.remove("typInput");
	  } else {
		tr[i].style.display = "none";
		tr[i].classList.add("typInput");
	  }
    }
  }
}
function searchByInstitut(searchID="institutInput", searchIn="3") {
  // Declare variables
  var input, filter, table, tr, td, i;
  input = document.getElementById(searchID);
  filter = input.value.toUpperCase();
  table = document.getElementById("myTableFK");
  tr = table.getElementsByTagName("tr");

  // Loop through all table rows, and hide those who don't match the search query
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[parseInt(searchIn)];
    if (td) {
      if (td.innerHTML.toUpperCase().indexOf(filter) > -1) {
		tr[i].style.display = "";
		tr[i].classList.remove("institutInput");
	  } else {
		tr[i].style.display = "none";
		tr[i].classList.add("institutInput");
	  }
    }
  }
}
function searchByFachgebiet(searchID="fachgebietInput", searchIn="4") {
  // Declare variables
  var input, filter, table, tr, td, i;
  input = document.getElementById(searchID);
  filter = input.value.toUpperCase();
  table = document.getElementById("myTableFK");
  tr = table.getElementsByTagName("tr");

  // Loop through all table rows, and hide those who don't match the search query
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[parseInt(searchIn)];
    if (td) {
      if (td.innerHTML.toUpperCase().indexOf(filter) > -1) {
		tr[i].style.display = "";
		tr[i].classList.remove("fachgebietInput");
	  } else {
		tr[i].style.display = "none";
		tr[i].classList.add("fachgebietInput");
	  }
    }
  }
}
function searchByPincodesFK(searchID="plzInputFK", searchIn="5") {
  // Declare variables
  var input, filter, table, tr, td, i;
  input = document.getElementById(searchID);
  filter = input.value.toUpperCase();
  table = document.getElementById("myTableFK");
  tr = table.getElementsByTagName("tr");

  // Loop through all table rows, and hide those who don't match the search query
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[parseInt(searchIn)];
    if (td) {
      if (td.innerHTML.toUpperCase().indexOf(filter) > -1) {
		tr[i].style.display = "";
		tr[i].classList.remove("plzInputFK");
	  } else {
		tr[i].style.display = "none";
		tr[i].classList.add("plzInputFK");
	  }
    }
  }
}
function searchBycityFK(searchID="cityInputFK", searchIn="6") {
  // Declare variables
  var input, filter, table, tr, td, i;
  input = document.getElementById(searchID);
  filter = input.value.toUpperCase();
  table = document.getElementById("myTableFK");
  tr = table.getElementsByTagName("tr");

  // Loop through all table rows, and hide those who don't match the search query
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[parseInt(searchIn)];
    if (td) {
      if (td.innerHTML.toUpperCase().indexOf(filter) > -1) {
		tr[i].style.display = "";
		tr[i].classList.remove("cityInputFK");
	  } else {
		tr[i].style.display = "none";
		tr[i].classList.add("cityInputFK");
	  }
    }
  }
}



//Suchfunktionen Kunden
function searchByFirstName(searchID="FirstNameInput", searchIn="0") {
  // Declare variables
  var input, filter, table, tr, td, i;
  input = document.getElementById(searchID);
  filter = input.value.toUpperCase();
  table = document.getElementById("myTable");
  tr = table.getElementsByTagName("tr");

  // Loop through all table rows, and hide those who don't match the search query
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[parseInt(searchIn)];
    if (td) {
      if (td.innerHTML.toUpperCase().indexOf(filter) > -1) {
		tr[i].style.display = "";
		tr[i].classList.remove("FirstNameInput");
	  } else {
		tr[i].style.display = "none";
		tr[i].classList.add("FirstNameInput");
	  }
    }
  }
}
function searchByLastName(searchID="LastNameInput", searchIn="1") {
  // Declare variables
  var input, filter, table, tr, td, i;
  input = document.getElementById(searchID);
  filter = input.value.toUpperCase();
  table = document.getElementById("myTable");
  tr = table.getElementsByTagName("tr");

  // Loop through all table rows, and hide those who don't match the search query
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[parseInt(searchIn)];
    if (td) {
      if (td.innerHTML.toUpperCase().indexOf(filter) > -1) {
		tr[i].style.display = "";
		tr[i].classList.remove("LastNameInput");
	  } else {
		tr[i].style.display = "none";
		tr[i].classList.add("LastNameInput");
	  }
    }
  }
}
function searchByPincodes(searchID="plzInput", searchIn="3") {
  // Declare variables
  var input, filter, table, tr, td, i;
  input = document.getElementById(searchID);
  filter = input.value.toUpperCase();
  table = document.getElementById("myTable");
  tr = table.getElementsByTagName("tr");

  // Loop through all table rows, and hide those who don't match the search query
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[parseInt(searchIn)];
    if (td) {
      if (td.innerHTML.toUpperCase().indexOf(filter) > -1) {
		tr[i].style.display = "";
		tr[i].classList.remove("plzInput");
	  } else {
		tr[i].style.display = "none";
		tr[i].classList.add("plzInput");
	  }
    }
  }
}
function searchBycity(searchID="cityInput", searchIn="4") {
  // Declare variables
  var input, filter, table, tr, td, i;
  input = document.getElementById(searchID);
  filter = input.value.toUpperCase();
  table = document.getElementById("myTable");
  tr = table.getElementsByTagName("tr");

  // Loop through all table rows, and hide those who don't match the search query
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[parseInt(searchIn)];
    if (td) {
      if (td.innerHTML.toUpperCase().indexOf(filter) > -1) {
		tr[i].style.display = "";
		tr[i].classList.remove("cityInput");
	  } else {
		tr[i].style.display = "none";
		tr[i].classList.add("cityInput");
	  }
    }
  }
}

function searchByMitgliedschaft(searchID="mitgliedschaftInput", searchIn="2") {
  // Declare variables
  var input, filter, table, tr, td, i;
  input = document.getElementById(searchID);
  filter = input.value.toUpperCase();
  table = document.getElementById("myTable");
  tr = table.getElementsByTagName("tr");

  // Loop through all table rows, and hide those who don't match the search query
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[parseInt(searchIn)];
    if (td) {
      if (td.innerHTML.toUpperCase().indexOf(filter) > -1) {
		tr[i].style.display = "";
		tr[i].classList.remove("mitgliedschaftInput");
	  } else {
		tr[i].style.display = "none";
		tr[i].classList.add("mitgliedschaftInput");
	  }
    }
  }
}









function loadData() {
	openNav();
	var typ = document.getElementById("suchtyp").value;
	frappe.call({
		method: 'touche.touche.page.touche_suchmaske.touche_suchmaske.get_all_infos',
		args: {
			"typ": typ
		},
		callback: function(r) {
			if (r.message) {
				//console.log(r.message);
				createTableWithContent(r.message);
				
			} 
		}
	});
}

function createTableWithContent(datas) {
	if (document.getElementById("suchtyp").value == "Fachkontakte") {
		var tabelle = document.getElementById("myTableFK");

		var rowCount = tabelle.rows.length;
		for (var i = rowCount - 1; i > 0; i--) {
			tabelle.deleteRow(i);
		}
		for (var i = 0; i < datas.length; i++) {
			crateTableContentElementFK(datas[i]["vorname"], datas[i]["nachname"], datas[i]["typ"], datas[i]["institut"], datas[i]["fachgebiet"], datas[i]["plz"], datas[i]["ort"], datas[i]["name"]);
		}
		closeNav();
	}
	if (document.getElementById("suchtyp").value == "Kunden") {
		var tabelle = document.getElementById("myTable");

		var rowCount = tabelle.rows.length;
		for (var i = rowCount - 1; i > 0; i--) {
			tabelle.deleteRow(i);
		}
		for (var i = 0; i < datas.length; i++) {
			crateTableContentElement(datas[i]["vorname"], datas[i]["nachname"], datas[i]["status_mitgliedschaft"], datas[i]["plz"], datas[i]["ort"], datas[i]["name"]);
		}
		closeNav();
	}
}

function crateTableContentElementFK(first_name, last_name, typ, institut, fachgebiet, pincode, city, referenz) {
	//console.log(name+" "+address+" "+pincode+" "+city);
	var tabelle = document.getElementById("myTableFK");
	
	var tr = document.createElement("tr");
	
	var td_first_name = document.createElement("td");
	var td_last_name = document.createElement("td");
	var td_typ = document.createElement("td");
	var td_institut = document.createElement("td");
	var td_fachgebiet = document.createElement("td");
	var td_pincode = document.createElement("td");
	var td_city = document.createElement("td");
	
	var td_first_name_txt = document.createTextNode(first_name);
	var td_last_name_txt = document.createTextNode(last_name);
	var td_typ_txt = document.createTextNode(typ);
	var td_institut_txt = document.createTextNode(institut);
	var td_fachgebiet_txt = document.createTextNode(fachgebiet);
	var td_pincode_txt = document.createTextNode(pincode);
	var td_city_txt = document.createTextNode(city);
	
	td_first_name.appendChild(td_first_name_txt);
	td_last_name.appendChild(td_last_name_txt);
	td_typ.appendChild(td_typ_txt);
	td_institut.appendChild(td_institut_txt);
	td_fachgebiet.appendChild(td_fachgebiet_txt);
	td_pincode.appendChild(td_pincode_txt);
	td_city.appendChild(td_city_txt);
	
	tr.onclick = function() { 
		window.location = '/desk#Form/Fachkontakt/' + referenz;
	};
	
	tr.appendChild(td_first_name);
	tr.appendChild(td_last_name);
	tr.appendChild(td_typ);
	tr.appendChild(td_institut);
	tr.appendChild(td_fachgebiet);
	tr.appendChild(td_pincode);
	tr.appendChild(td_city);
	
	tabelle.appendChild(tr);
	
}

function crateTableContentElement(first_name, last_name, mitglied, pincode, city, referenz) {
	//console.log(name+" "+address+" "+pincode+" "+city);
	var tabelle = document.getElementById("myTable");
	
	var tr = document.createElement("tr");
	
	var td_first_name = document.createElement("td");
	var td_last_name = document.createElement("td");
	var td_mitglied = document.createElement("td");
	var td_pincode = document.createElement("td");
	var td_city = document.createElement("td");
	
	var td_first_name_txt = document.createTextNode(first_name);
	var td_last_name_txt = document.createTextNode(last_name);
	var td_mitglied_txt = document.createTextNode(mitglied);
	var td_pincode_txt = document.createTextNode(pincode);
	var td_city_txt = document.createTextNode(city);
	
	td_first_name.appendChild(td_first_name_txt);
	td_last_name.appendChild(td_last_name_txt);
	td_mitglied.appendChild(td_mitglied_txt);
	td_pincode.appendChild(td_pincode_txt);
	td_city.appendChild(td_city_txt);
	
	tr.onclick = function() { 
		window.location = '/desk#Form/Customer/' + referenz;
	};
	
	tr.appendChild(td_first_name);
	tr.appendChild(td_last_name);
	tr.appendChild(td_mitglied);
	tr.appendChild(td_pincode);
	tr.appendChild(td_city);
	
	tabelle.appendChild(tr);
	
}