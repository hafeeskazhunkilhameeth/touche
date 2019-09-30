// Copyright (c) 2016, libracore and contributors
// For license information, please see license.txt
/* eslint-disable */
frappe.query_reports["Vereinnahmte ER"] = {
	"filters": [

	],
	"formatter": function(value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);

		if ((data["Konto"] == "3 - Erträge")||(data["Konto"] == "Total")||(data["Konto"] == "4 - Aufwände")||(data["Konto"] == "Gewinn / Verlust")) {
			value = $(`<span>${value}</span>`);
			var $value = $(value).css("font-weight", "bold");
			value = $value.wrap("<p></p>").parent().html();
		}

		return value;
	}
}
