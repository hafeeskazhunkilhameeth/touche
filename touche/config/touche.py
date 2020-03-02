from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Beratungen"),
			"items": [
				{
					"type": "doctype",
					"name": "Touche Fall",
					"label": _("Fall"),
					"description": _("Fall")
				},
				{
					"type": "doctype",
					"name": "Touche Beratung",
					"label": _("Beratung"),
					"description": _("Beratung")
				}
			]
		},
		{
			"label": _("Kunden / Kontakte / Lieferanten"),
			"items": [
				{
					"type": "doctype",
					"name": "Customer",
					"label": _("Customer"),
					"description": _("Customers")
				},
				{
					"type": "doctype",
					"name": "Fachkontakt",
					"label": _("Fachkontakt"),
					"description": _("Fachkontakt")
				},
				{
					"type": "doctype",
					"name": "Supplier",
					"label": _("Supplier"),
					"description": _("Suppliers")
				},
				{
					"type": "doctype",
					"name": "Contact",
					"label": _("Allgemeiner Kontakt"),
					"description": _("Kontakt")
				},
				{
					"type": "doctype",
					"name": "Address",
					"label": _("Adressen"),
					"description": _("Adressen")
				}
			]
		},
		{
			"label": _("Rechnungsstellung"),
			"items": [
				{
				   "type": "page",
				   "name": "rechnungslauf",
				   "label": _("Rechnungslauf"),
				   "description": _("Rechnungslauf")
				},
				{
					"type": "doctype",
					"name": "Sales Invoice",
					"label": _("Kundenrechnungen"),
					"description": _("Kundenrechnungen")
				},
				{
					"type": "doctype",
					"name": "Purchase Invoice",
					"label": _("Lieferantenrechnung"),
					"description": _("Lieferantenrechnung")
				},
				{
					"type": "doctype",
					"name": "Journal Entry",
					"label": _("Journal Entry"),
					"description": _("Journal Entry")
				},
				{
					"type": "doctype",
					"name": "Account",
					"icon": "fa fa-sitemap",
					"label": _("Chart of Accounts"),
					"route": "Tree/Account",
					"description": _("Tree of financial accounts.")
				},
				{
					"type": "report",
					"name":"General Ledger",
					"doctype": "GL Entry",
					"is_query_report": True
				},
				{
					"type": "report",
					"name":"Vereinnahmte ER",
					"doctype": "Sales Invoice",
					"is_query_report": True
				}
			]
		},
		{
			"label": _("Diverses"),
			"items": [
				{
					"type": "report",
					"name":"Adressen Mitglieder Zeitschrift",
					"doctype": "Address",
					"is_query_report": True
				},
				{
				   "type": "page",
				   "name": "touche-suchmaske",
				   "label": _("Suchmaske"),
				   "description": _("Suchmaske")
				},
				{
					"type": "report",
					"name":"BSV",
					"doctype": "Touche Fall",
					"is_query_report": True,
					"label": _("BSV Report")
				}
			]
		}
	]