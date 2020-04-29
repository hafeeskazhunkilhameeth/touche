// Copyright (c) 2016, libracore and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["BSV"] = {
	"filters": [
		{
			"fieldname": "year",
			"label": __("Year"),
			"fieldtype": "Int",
			"default": new Date().getFullYear(),
			"reqd": 1
		},
		{
			"fieldname": "customer",
			"label": __("Customer"),
			"fieldtype": "Link",
			"options": "Customer"
		},
		{
			"fieldname": "iv_leistungen",
			"label": __("IV-Leistungen"),
			"fieldtype": "Select",
			"options": ["n/a", "IV", "AHV", "Abklären", "Ehemalig IV", "nicht berechtigt"]
		},
		{
			"fieldname": "auswertungstyp",
			"label": __("Auswertungs-Typ"),
			"fieldtype": "Select",
			"options": ["Beratungsstunden", "nach Kanton", "Neukunden"],
			"reqd": 1
		},
		{
			"fieldname": "beratungstyp",
			"label": __("Beratung an"),
			"fieldtype": "Select",
			"options": ["Betroffener", "Angehöriger / Bezugsperson"],
			"reqd": 1
		}
	]
};
