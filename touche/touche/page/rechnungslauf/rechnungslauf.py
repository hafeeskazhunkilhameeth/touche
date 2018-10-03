from __future__ import unicode_literals
import frappe, os, json
from frappe import throw, _
from frappe import utils
from frappe.contacts.doctype.address.address import get_default_address
from touche import esr

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
		mitglieder_rechnungen = create_invoice(mitglieder, "Mitglied")
			
		#anwalte
		anwalte = frappe.get_list("Fachkontakt", fields=["customer", "betrag", "anrede"], filters =
			[["rechnung", "=", "1"],
			["typ", "=", "Jurist"],
			["deaktiviert", "!=", "1"]])
			
		anwalt_rechnungen = create_invoice(anwalte, "Anwalt")
		
		#kanzleien
		kanzleien = frappe.get_list("Fachkontakt", fields=["customer", "betrag", "anrede"], filters =
			[["rechnung", "=", "1"],
			["typ", "=", "Kanzlei"],
			["deaktiviert", "!=", "1"]])
			
		kanzlei_rechnungen = create_invoice(kanzleien, "Kanzlei")
		
		return mitglieder_rechnungen, anwalt_rechnungen, kanzlei_rechnungen
		
	if lauf == "Mitglieder":
		if typ == "Alle":
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
		else:
			mitglieder_ohne_austritt = frappe.get_list("Customer", fields=["name", "status_mitgliedschaft"], filters =
				[["status_mitgliedschaft", "=", typ],
				["disabled", "!=", "1"],
				["name", "!=", "Guest"],
				["austritt", "<", "1900-01-01"]])
			
			today = utils.today()
			cur_year = today.split("-")[0]
			end_of_year = cur_year + "-12-31"
			mitglieder_mit_austritt = frappe.get_list("Customer", fields=["name", "status_mitgliedschaft"], filters =
				[["status_mitgliedschaft", "=", typ],
				["disabled", "!=", "1"], 
				["austritt", ">=", end or end_of_year]])
		
		mitglieder = mitglieder_ohne_austritt + mitglieder_mit_austritt
		mitglieder_rechnungen = create_invoice(mitglieder, "Mitglied")
		return mitglieder_rechnungen
			
	if lauf == "Anwalte":
		anwalte = frappe.get_list("Fachkontakt", fields=["customer", "betrag", "anrede"], filters =
			[["rechnung", "=", "1"],
			["typ", "=", "Jurist"],
			["deaktiviert", "!=", "1"]])
		anwalt_rechnungen = create_invoice(anwalte, "Anwalt")
		return anwalt_rechnungen
			
	if lauf == "Kanzleien":
		kanzleien = frappe.get_list("Fachkontakt", fields=["customer", "betrag", "anrede"], filters =
			[["rechnung", "=", "1"],
			["typ", "=", "Kanzlei"],
			["deaktiviert", "!=", "1"]])
		kanzlei_rechnungen = create_invoice(kanzleien, "Kanzlei")
		return kanzlei_rechnungen

def create_invoice(customers, typ):
	customer_name = ""
	customer_address = ""
	item = ""
	invoice_txt = ""
	invoices = []
	
	for customer in customers:
		if typ == "Mitglied":
			customer_name = customer['name']
			customer_address = get_default_address(doctype="Customer", name=customer_name)
			if customer['status_mitgliedschaft'] == "Einzel":
				item = "Einzel-Mitglied Beitrag"
			if customer['status_mitgliedschaft'] == "Familie":
				item = "Familien-Mitglied Beitrag"
			if customer['status_mitgliedschaft'] == "Kollektiv":
				item = "Kollektiv-Mitglied Beitrag"
		if typ == "Anwalt":
			return
		
		if typ == "Kanzlei":
			return
	
		sales_invoice = frappe.new_doc("Sales Invoice")
		sales_invoice.update({
			"customer": customer_name,
			"customer_address": customer_address,
			"shipping_address_name": customer_address,
			"delivery_date": utils.today(),
			"items": [{
				"item_code": item,
				"qty": "1"
			}]
		})
		sales_invoice.flags.ignore_mandatory = True
		sales_invoice.save(ignore_permissions=True)
		referencenumber = sales_invoice.name.split("-")[1]
		sales_invoice.update({
			"esr_reference": esr.get_reference_number(referencenumber),
			"esr_code": esr.generateCodeline(sales_invoice.grand_total, esr.get_reference_number(referencenumber), "01154388")
		})
		sales_invoice.save(ignore_permissions=True)
		sales_invoice.submit()
		frappe.db.commit()
		invoices.append(sales_invoice.name)
	return invoices