// Copyright (c) 2016, libracore and contributors
// For license information, please see license.txt
/* eslint-disable */
frappe.query_reports["Vereinnahmte ER"] = {
	"filters": [

	],
	"formatter":function (row, cell, value, columnDef, dataContext, default_formatter) {
		value = default_formatter(row, cell, value, columnDef, dataContext);
		if (columnDef.id == __("Konto") && (dataContext["Konto"] == "3 - Erträge" || dataContext["Konto"] == "4 - Aufwände" || dataContext["Konto"] == "Total" || dataContext["Konto"] == "Gewinn / Verlust")) {
				value = "<span style='font-weight:bold!important;'>" + value + "</span>";
				_row = true;
		}
		if (row == 7 || row == 31 || row == 33) {
			value = "<span style='font-weight:bold!important;'>" + value + "</span>";
		}
		return value;
	}
}
