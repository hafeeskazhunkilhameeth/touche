from __future__ import unicode_literals
import frappe, os, json
from frappe import throw, _
from frappe import utils
from frappe.contacts.doctype.address.address import get_default_address
from touche import esr
from frappe.utils.background_jobs import enqueue
from datetime import datetime
from PyPDF2 import PdfFileWriter

@frappe.whitelist()
def rechnungslauf(lauf=None, typ=None, end=None):
	# if lauf == "Alle":
		# mitglieder_ohne_austritt = frappe.get_list("Customer", fields=["name", "status_mitgliedschaft"], filters =
			# [["status_mitgliedschaft", "!=", "Ehemalig"],
			# ["status_mitgliedschaft", "!=", "Gegenseitig"],
			# ["status_mitgliedschaft", "!=", "Gratis"],
			# ["status_mitgliedschaft", "!=", "Beratungskontakt"],
			# ["status_mitgliedschaft", "!=", "Fachkontakt"],
			# ["disabled", "!=", "1"],
			# ["name", "!=", "Guest"],
			# ["austritt", "<", "1900-01-01"]])
		
		# today = utils.today()
		# cur_year = today.split("-")[0]
		# end_of_year = cur_year + "-12-31"
		# mitglieder_mit_austritt = frappe.get_list("Customer", fields=["name", "status_mitgliedschaft"], filters =
			# [["status_mitgliedschaft", "!=", "Ehemalig"],
			# ["status_mitgliedschaft", "!=", "Gegenseitig"],
			# ["status_mitgliedschaft", "!=", "Gratis"],
			# ["status_mitgliedschaft", "!=", "Beratungskontakt"],
			# ["status_mitgliedschaft", "!=", "Fachkontakt"],
			# ["disabled", "!=", "1"], 
			# ["austritt", ">=", end or end_of_year]])
			
		# mitglieder = mitglieder_ohne_austritt + mitglieder_mit_austritt
		# mitglieder_rechnungen = create_invoice(mitglieder, "Mitglied")
			
		# #anwalte
		# anwalte = frappe.get_list("Fachkontakt", fields=["customer", "betrag", "anrede"], filters =
			# [["rechnung", "=", "1"],
			# ["typ", "=", "Jurist"],
			# ["deaktiviert", "!=", "1"]])
			
		# anwalt_rechnungen = create_invoice(anwalte, "Anwalt")
		
		# #kanzleien
		# kanzleien = frappe.get_list("Fachkontakt", fields=["customer", "betrag", "anrede"], filters =
			# [["rechnung", "=", "1"],
			# ["typ", "=", "Kanzlei"],
			# ["deaktiviert", "!=", "1"]])
			
		# kanzlei_rechnungen = create_invoice(kanzleien, "Kanzlei")
		
		# return mitglieder_rechnungen, anwalt_rechnungen, kanzlei_rechnungen
		
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
		#return mitglieder_rechnungen
			
	if lauf == "Anwalte":
		anwalte = frappe.get_list("Fachkontakt", fields=["customer", "betrag", "anrede"], filters =
			[["rechnung", "=", "1"],
			["typ", "=", "Jurist"],
			["deaktiviert", "!=", "1"]])
		anwalt_rechnungen = create_invoice(anwalte, "Anwalt")
		#return anwalt_rechnungen
			
	if lauf == "Kanzleien":
		kanzleien = frappe.get_list("Fachkontakt", fields=["customer", "betrag", "anrede"], filters =
			[["rechnung", "=", "1"],
			["typ", "=", "Kanzlei"],
			["deaktiviert", "!=", "1"]])
		kanzlei_rechnungen = create_invoice(kanzleien, "Kanzlei")
		#return kanzlei_rechnungen

def create_invoice(customers, typ):
	frappe.publish_realtime("invoice_progress", {"progress": "0"}, user=frappe.session.user)
	enqueue(_create_invoice, queue='default', timeout=6000, event='create_invoice', customers=customers, typ=typ)
	#frappe.msgprint(_('''Invoices will be created in the background.'''))
	
		
def _create_invoice(customers, typ):
	customer_name = ""
	customer_address = ""
	item = ""
	rate = ""
	invoice_txt = ""
	invoices = []
	total_records = len(customers)
	created_records = 0
	
	if len(customers) > 0:
		for customer in customers:
			sales_invoice = frappe.new_doc("Sales Invoice")
			if typ == "Mitglied":
				customer_name = customer['name']
				customer_address = get_default_address(doctype="Customer", name=customer_name)
				if customer['status_mitgliedschaft'] == "Einzel":
					item = "Einzel-Mitglied Beitrag"
				if customer['status_mitgliedschaft'] == "Familie":
					item = "Familien-Mitglied Beitrag"
				if customer['status_mitgliedschaft'] == "Kollektiv":
					item = "Kollektiv-Mitglied Beitrag"
				sales_invoice.update({
					"customer": customer_name,
					"customer_address": customer_address,
					"shipping_address_name": customer_address,
					"delivery_date": utils.today(),
					"due_date": utils.add_days(utils.today(), 60),
					"items": [{
						"item_code": item,
						"qty": "1"
					}]
				})
				
			else:
				customer_name = customer['customer']
				customer_address = get_default_address(doctype="Customer", name=customer_name)
				item = "Soli-Beitrag"
				rate = customer['betrag']
				sales_invoice.update({
					"customer": customer_name,
					"customer_address": customer_address,
					"shipping_address_name": customer_address,
					"delivery_date": utils.today(),
					"due_date": utils.add_days(utils.today(), 60),
					"items": [{
						"item_code": item,
						"qty": "1",
						"rate": rate
					}]
				})
		
			sales_invoice.flags.ignore_mandatory = True
			sales_invoice.save(ignore_permissions=True)
			referencenumber = sales_invoice.name.split("-")[1]
			sales_invoice.update({
				"esr_reference": esr.get_reference_number(referencenumber),
				"esr_code": esr.generateCodeline(sales_invoice.grand_total, referencenumber, "010154388")
			})
			sales_invoice.save(ignore_permissions=True)
			sales_invoice.submit()
			frappe.db.commit()
			invoices.append([sales_invoice.name, item, sales_invoice.grand_total])
			created_records += 1
			frappe.publish_realtime("invoice_progress", {"progress": str(int(created_records * 100/total_records))}, user=frappe.session.user)
			
		frappe.publish_realtime("invoices", {"invoices": invoices}, user=frappe.session.user)
	else:
		frappe.publish_realtime("invoices", {}, user=frappe.session.user)
	#return invoices
	
	
@frappe.whitelist()
def list_all_pdfs():
	from os import listdir
	from os.path import isfile, join
	path = "/home/frappe/frappe-bench/sites/assets/touche/sinvs_for_print/"
	onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
	return onlyfiles 
	
@frappe.whitelist()
def remove_downloaded_pdf():
	path = "/home/frappe/frappe-bench/sites/assets/touche/sinvs_for_print/"
	for filename in os.listdir(path):
		os.remove(str(path) + str(filename))


@frappe.whitelist()
def createSammelPDF():
	frappe.publish_realtime("pdf_progress", {"progress": "0"}, user=frappe.session.user)
	enqueue(_createSammelPDF, queue='default', timeout=6000, event='Generierung Sammel-PDF', valuta=utils.today(), printformat='Mitglieder Rechnung')
	#frappe.msgprint(_('''Die PDFs werden erstellt.'''))
	
def _createSammelPDF(valuta, printformat):
	sql_query = ("""SELECT `name` FROM `tabSales Invoice` WHERE `posting_date` = '{0}' AND `docstatus` = 1""".format(valuta))
	sinvs = frappe.db.sql(sql_query, as_dict=True)
	#frappe.msgprint(str(len(sinvs)))
	print_sinv = []
	loop_controller = 1
	qty_controller = 0
	progress = 0
	for sinv in sinvs:
		progress += 1
		print_sinv.append(sinv)
		qty_controller += 1
		if qty_controller == 100:
			# run bind job for 100 batch
			if len(print_sinv) > 0:
				now = datetime.now()
				bind_source = "/assets/touche/sinvs_for_print/sammel_pdf_vom_{valuta}-{loop}.pdf".format(valuta=valuta, loop=loop_controller)
				physical_path = "/home/frappe/frappe-bench/sites" + bind_source
				print_bind(print_sinv, format=printformat, dest=str(physical_path))
				qty_controller = 0
				loop_controller += 1
				print_sinv = []
				frappe.publish_realtime("pdf_progress", {"progress": str(int(progress * 100/len(sinvs)))}, user=frappe.session.user)
				
	# run bind job for rest batch
	if len(print_sinv) > 0:
		now = datetime.now()
		bind_source = "/assets/touche/sinvs_for_print/sammel_pdf_vom_{valuta}-{loop}.pdf".format(valuta=valuta, loop=loop_controller)
		physical_path = "/home/frappe/frappe-bench/sites" + bind_source
		print_bind(print_sinv, format=printformat, dest=str(physical_path))
		frappe.publish_realtime("pdf_progress", {"progress": str(int(progress * 100/len(sinvs)))}, user=frappe.session.user)
		
		
		
# this function will bind a pdf from all provided sales invoices (list of names)
def print_bind(sales_invoices, format=None, dest=None):
	# Concatenating pdf files
	output = PdfFileWriter()
	progress = 0
	for sales_invoice in sales_invoices:
		output = frappe.get_print("Sales Invoice", sales_invoice, format, as_pdf = True, output = output)
		print("append to output")
		progress += 1
		frappe.publish_realtime("print_progress", {"progress": str(int(progress * 100/len(sales_invoices)))}, user=frappe.session.user)
	if dest != None:
		if isinstance(dest, str): # when dest is a file path
			destdir = os.path.dirname(dest)
			if destdir != '' and not os.path.isdir(destdir):
				os.makedirs(destdir)
			with open(dest, "wb") as w:
				output.write(w)
		else: # when dest is io.IOBase
			output.write(dest)
			print("first return")
		return
	else:
		print("second return")
		return output
