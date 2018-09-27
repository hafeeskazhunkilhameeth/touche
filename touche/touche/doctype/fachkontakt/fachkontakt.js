// Copyright (c) 2018, libracore and contributors
// For license information, please see license.txt

frappe.ui.form.on('Fachkontakt', {
	refresh: function(frm) {
		if(!frm.doc.__islocal) {
			frappe.dynamic_link = {doc: frm.doc, fieldname: 'customer', doctype: 'Customer'};
			frappe.contacts.render_address_and_contact(frm);
		} else {
			frappe.contacts.clear_address_and_contact(frm);
		}
	}
});
