// Copyright (c) 2016, libracore and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Mitglieder Adressliste"] = {
	"filters": [
		{
			"fieldname":"party_name",
			"label": __("Party Name"),
			"fieldtype": "Dynamic Link",
			"get_options": function() {
				let party_type = frappe.query_report.get_filter_value('party_type');
				if(!party_type) {
					frappe.throw(__("Please select Party Type first"));
				}
				return party_type;
			}
		}
	]
};