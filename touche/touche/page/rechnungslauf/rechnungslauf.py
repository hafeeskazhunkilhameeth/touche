from __future__ import unicode_literals
import frappe, os, json
from frappe import throw, _
from frappe import utils

@frappe.whitelist()
def rechnungslauf(lauf=None, typ=None, end=None):
	if lauf == "Alle":
		mitglieder_ohne_austritt = frappe.get_list("Customer", fields=["name", "status_mitgliedschaft"], filters =
			[["status_mitgliedschaft", "!=", "Ehemalig"],
			["status_mitgliedschaft", "!=", "Gegenseitig"],
			["status_mitgliedschaft", "!=", "Gratis"],
			["status_mitgliedschaft", "!=", "Beratungskontakt"],
			["status_mitgliedschaft", "!=", "Fachkontakt"],
			["disabled", "!=", "1"],
			["name", "!=", "Guest"],
			["austritt", "<", "1900-01-01"]])
		
		today = utils.today()
		cur_year = today.split("-")[0]
		end_of_year = cur_year + "-12-31"
		mitglieder_mit_austritt = frappe.get_list("Customer", fields=["name", "status_mitgliedschaft"], filters =
			[["status_mitgliedschaft", "!=", "Ehemalig"],
			["status_mitgliedschaft", "!=", "Gegenseitig"],
			["status_mitgliedschaft", "!=", "Gratis"],
			["status_mitgliedschaft", "!=", "Beratungskontakt"],
			["status_mitgliedschaft", "!=", "Fachkontakt"],
			["disabled", "!=", "1"], 
			["austritt", ">=", end or end_of_year]])
			
		mitglieder = mitglieder_ohne_austritt + mitglieder_mit_austritt
		create_invoice(mitglieder)
			
		#anwalte
		anwalte = frappe.get_list("Fachkontakt", fields=["customer", "betrag", "anrede"], filters =
			[["rechnung", "=", "1"],
			["typ", "=", "Jurist"],
			["deaktiviert", "!=", "1"]])
		
		#kanzleien
		kanzleien = frappe.get_list("Fachkontakt", fields=["customer", "betrag", "anrede"], filters =
			[["rechnung", "=", "1"],
			["typ", "=", "Kanzlei"],
			["deaktiviert", "!=", "1"]])
		
		return mitglieder, anwalte, kanzleien
		
	if lauf == "Mitglieder":
		mitglieder_ohne_austritt = frappe.get_list("Customer", fields=["name", "status_mitgliedschaft"], filters =
			[["status_mitgliedschaft", "!=", "Ehemalig"],
			["status_mitgliedschaft", "!=", "Gegenseitig"],
			["status_mitgliedschaft", "!=", "Gratis"],
			["status_mitgliedschaft", "!=", "Beratungskontakt"],
			["status_mitgliedschaft", "!=", "Fachkontakt"],
			["disabled", "!=", "1"],
			["name", "!=", "Guest"],
			["austritt", "<", "1900-01-01"]])
		
		today = utils.today()
		cur_year = today.split("-")[0]
		end_of_year = cur_year + "-12-31"
		mitglieder_mit_austritt = frappe.get_list("Customer", fields=["name", "status_mitgliedschaft"], filters =
			[["status_mitgliedschaft", "!=", "Ehemalig"],
			["status_mitgliedschaft", "!=", "Gegenseitig"],
			["status_mitgliedschaft", "!=", "Gratis"],
			["status_mitgliedschaft", "!=", "Beratungskontakt"],
			["status_mitgliedschaft", "!=", "Fachkontakt"],
			["disabled", "!=", "1"], 
			["austritt", ">=", end or end_of_year]])
			
	if lauf == "Anwalt":
		anwalte = frappe.get_list("Fachkontakt", fields=["customer", "betrag", "anrede"], filters =
			[["rechnung", "=", "1"],
			["typ", "=", "Jurist"],
			["deaktiviert", "!=", "1"]])
			
	if lauf == "Kanzlei":
		kanzleien = frappe.get_list("Fachkontakt", fields=["customer", "betrag", "anrede"], filters =
			[["rechnung", "=", "1"],
			["typ", "=", "Kanzlei"],
			["deaktiviert", "!=", "1"]])

def create_invoice(customers):
	# sales_invoice = frappe.new_doc("Sales Invoice")
	# sales_invoice.update({
		# "customer": customer,
		# "customer_address": billing,
		# "shipping_address_name": shipping,
		# "delivery_date": utils.today(),
		# "pflanzenfreund_abo": pflanzenfreund_abo.name,
		# "taxes_and_charges": "Schweiz normal (302) - GCM",
		# "items": [{
			# "item_code": abo,
			# "qty": "1"
		# }],
		# "taxes": [{
			# "charge_type": "On Net Total",
			# "account_head": "2200 - Umsatzsteuer - GCM",
			# "cost_center": "Haupt - GCM",
			# "rate": "7.7",
			# "description": "Inkl. 7.7% MwSt"
		# }]
	# })
	# sales_invoice.flags.ignore_mandatory = True
	# sales_invoice.save(ignore_permissions=True)
	# referencenumber = sales_invoice.name.split("-")[1]
	# sales_invoice.update({
		# "esr_reference": esr.get_reference_number(referencenumber),
		# "esr_code": esr.generateCodeline(sales_invoice.grand_total, esr.get_reference_number(referencenumber), "013100113")
	# })
	# sales_invoice.save(ignore_permissions=True)
	# sales_invoice.submit()
# frappe.db.commit()
	return