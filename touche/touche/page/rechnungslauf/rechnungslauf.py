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
		return mitglieder
			
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
		
	if lauf == "Mitglieder":
		mitglieder_ohne_austritt = frappe.get_list("Customer", fields=["name"], filters =
			[["status_mitgliedschaft", "!=", "Ehemalig"],
			["status_mitgliedschaft", "!=", "Gegenseitig"],
			["status_mitgliedschaft", "!=", "Gratis"],
			["status_mitgliedschaft", "!=", "Beratungskontakt"],
			["status_mitgliedschaft", "!=", "Fachkontakt"],
			["disabled", "!=", "1"], 
			["austritt", "=", ""]])
		
		today = utils.today()
		cur_year = today.split("-")[0]
		end_of_year = cur_year + "-12-31"
		mitglieder_mit_austritt = frappe.get_list("Customer", fields=["name"], filters =
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
