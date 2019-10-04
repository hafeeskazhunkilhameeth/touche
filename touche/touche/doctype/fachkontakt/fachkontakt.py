# -*- coding: utf-8 -*-
# Copyright (c) 2018, libracore and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.contacts.address_and_contact import delete_contact_and_address
import functools

class Fachkontakt(Document):
	def onload(self):
		"""Load address and contacts in `__onload`"""
		load_address_and_contact(self)
		
	def on_trash(self):
		if self.customer:
			delete_contact_and_address('Customer', self.customer)
		else:
			delete_contact_and_address('Fachkontakt', self.name)

def load_address_and_contact(doc, key=None):
	"""Loads address list and contact list in `__onload`"""
	from frappe.contacts.doctype.address.address import get_address_display
	
	if doc.customer:
		filters = [
			["Dynamic Link", "link_doctype", "=", "Customer"],
			["Dynamic Link", "link_name", "=", doc.customer],
			["Dynamic Link", "parenttype", "=", "Address"],
		]
	else:
		filters = [
			["Dynamic Link", "link_doctype", "=", "Fachkontakt"],
			["Dynamic Link", "link_name", "=", doc.name],
			["Dynamic Link", "parenttype", "=", "Address"],
		]
	address_list = frappe.get_all("Address", filters=filters, fields=["*"])

	address_list = [a.update({"display": get_address_display(a)})
		for a in address_list]

	address_list = sorted(address_list,
		key = functools.cmp_to_key(lambda a, b:
			(int(a.is_primary_address - b.is_primary_address)) or
			(1 if a.modified - b.modified else 0)), reverse=True)

	doc.set_onload('addr_list', address_list)

	contact_list = []
	if doc.customer:
		filters = [
			["Dynamic Link", "link_doctype", "=", "Customer"],
			["Dynamic Link", "link_name", "=", doc.customer],
			["Dynamic Link", "parenttype", "=", "Contact"],
		]
	else:
		filters = [
			["Dynamic Link", "link_doctype", "=", "Fachkontakt"],
			["Dynamic Link", "link_name", "=", doc.name],
			["Dynamic Link", "parenttype", "=", "Contact"],
		]
	contact_list = frappe.get_all("Contact", filters=filters, fields=["*"])

	contact_list = sorted(contact_list,
		key = functools.cmp_to_key(lambda a, b:
			(int(a.is_primary_contact - b.is_primary_contact)) or
			(1 if a.modified - b.modified else 0)), reverse=True)

	doc.set_onload('contact_list', contact_list)