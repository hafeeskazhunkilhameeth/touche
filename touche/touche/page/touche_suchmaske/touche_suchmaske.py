# -*- coding: utf-8 -*-
# Copyright (c) 2017-2018, libracore and contributors
# License: AGPL v3. See LICENCE

from __future__ import unicode_literals
import frappe
from frappe import throw, _

@frappe.whitelist()
def get_all_infos(typ):
	if typ == "Fachkontakte":
		infos = []
		alle_fk = frappe.db.sql("""SELECT
									`name`,
									`typ`,
									`institut`,
									`med_spezialgebiet`,
									`disziplin`,
									`customer`
								FROM `tabFachkontakt`
								WHERE
									`deaktiviert` != 1""", as_dict=True)
									
		for fk in alle_fk:
			daten = {}
			
			daten['typ'] = fk.typ
			daten['institut'] = fk.institut or ''
			daten['name'] = fk.name
			#Fachgebiet
			if fk.typ == "Jurist":
				daten['fachgebiet'] = ""
			if fk.typ == "Mediziner":
				daten['fachgebiet'] = fk.med_spezialgebiet or ''
			if fk.typ == "Therapeut":
				daten['fachgebiet'] = fk.disziplin or ''
			if fk.typ == "Verband":
				daten['fachgebiet'] = ""
			if fk.typ == "Klinik":
				daten['fachgebiet'] = ""
			if fk.typ == "Kanzlei":
				daten['fachgebiet'] = ""
			if fk.typ == "Journalist / Medien":
				daten['fachgebiet'] = ""
			#Vorname / Nachname / ort / plz
			link = fk.name
			if fk.customer:
				link = fk.customer
			_daten = frappe.db.sql("""SELECT
										`contact`.`first_name` AS 'vorname',
										`contact`.`last_name` AS 'nachname',
										`address`.`pincode` AS 'plz',
										`address`.`city` AS 'ort'
									FROM (((`tabDynamic Link` AS `link`
									INNER JOIN `tabContact` AS `contact` ON `link`.`parent` = `contact`.`name`)
									INNER JOIN `tabDynamic Link` AS `adr_link` ON `link`.`link_name` = `adr_link`.`link_name`)
									INNER JOIN `tabAddress` AS `address` ON `adr_link`.`parent` = `address`.`name`)
									WHERE
										`link`.`link_name` = '{customer}'""".format(customer=link), as_dict=True)
			if len(_daten) > 0:
				_daten = _daten[0]
				daten['vorname'] = _daten.vorname or ''
				daten['nachname'] = _daten.nachname or ''
				daten['ort'] = _daten.ort or ''
				daten['plz'] = _daten.plz or ''
			else:
				daten['vorname'] = ''
				daten['nachname'] = ''
				daten['ort'] = ''
				daten['plz'] = ''
				
					
			infos.append(daten)
		return infos
		
	if typ == "Kunden":
		customer_query = """SELECT
								`customer`.`name` AS 'name',
								`customer`.`status_mitgliedschaft` AS 'status_mitgliedschaft',
								`contact`.`first_name` AS 'vorname',
								`contact`.`last_name` AS 'nachname',
								`address`.`pincode` AS 'plz',
								`address`.`city` AS 'ort'
							FROM ((((`tabCustomer` AS `customer`
							INNER JOIN `tabDynamic Link` AS `adr_link` ON `customer`.`name` = `adr_link`.`link_name`)
							INNER JOIN `tabAddress` AS `address` ON `adr_link`.`parent` = `address`.`name`)
							INNER JOIN `tabDynamic Link` AS `link` ON `customer`.`name` = `link`.`link_name`)
							INNER JOIN `tabContact` AS `contact` ON `link`.`parent` = `contact`.`name`)"""
		return frappe.db.sql(customer_query, as_dict=1)
		