// Copyright (c) 2018, libracore and contributors
// For license information, please see license.txt

frappe.ui.form.on('Touche Beratung', {
	refresh: function(frm) {

	},
	onload: function(frm) {
		if (frm.doc.__islocal) {
			cur_frm.set_value('bearbeiter', frappe.user.name);
		}
	}
});
