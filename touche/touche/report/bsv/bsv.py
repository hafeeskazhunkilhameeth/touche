# Copyright (c) 2013, libracore and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	columns, data = [], []
	if filters.auswertungstyp == 'Beratungsstunden':
		total_min = 0
		columns = ["Kunde:Link/Customer", "IV Leistung:Data", "Summe Zeitaufwand (in Minuten):Data"]
		customers = get_alle_kunden(filters)
		for customer in customers:
			alle_faelle_pro_kunde = get_alle_faelle_pro_kunde(customer.name)
			if alle_faelle_pro_kunde:
				beratungen = get_alle_beratungen_zu_faelle(alle_faelle_pro_kunde, filters)
				if beratungen:
					minuten = get_summe_in_min_basierend_auf_beratungen(beratungen)
					_data = []
					_data.append(customer.name)
					_data.append(customer.iv_status)
					_data.append(minuten)
					data.append(_data)
					total_min += minuten
		data.append(['', 'Total', total_min])
	if filters.auswertungstyp == 'nach Kanton':
		columns = ["Kanton:Data:150", "Anzahl:Data:150"]
		kantone = {
			'AG': 0,
			'AI': 0,
			'AR': 0,
			'BE': 0,
			'BL': 0,
			'BS': 0,
			'FR': 0,
			'GE': 0,
			'GL': 0,
			'GR': 0,
			'JU': 0,
			'LU': 0,
			'NE': 0,
			'NW': 0,
			'OW': 0,
			'SG': 0,
			'SH': 0,
			'SO': 0,
			'SZ': 0,
			'TG': 0,
			'TI': 0,
			'UR': 0,
			'VD': 0,
			'VS': 0,
			'ZG': 0,
			'ZH': 0,
			'Ausland': 0
		}
		for key in kantone:
			customers = get_alle_kunden_nach_kanton(filters, key)
			for customer in customers:
				faelle = get_alle_faelle_pro_kunde(customer.name)
				for fall in faelle:
					anz_beratungen = get_anzahl_beratungen_pro_fall(filters, fall[0])
					if anz_beratungen > 0:
						kantone[key] += 1
		for key in kantone:
			_data = []
			_data.append(str(key))
			_data.append(str(kantone[key]))
			data.append(_data)
			
	if filters.auswertungstyp == 'Neukunden':
		columns = ["Auswertung:Data:600"]
		anz = 0
		anz_betroffene = 0
		anz_angehoerige = 0
		customer_filter = ''
		if filters.iv_leistungen:
			customer_filter = """ AND `iv_status` = '{iv_leistungen}'""".format(iv_leistungen=filters.iv_leistungen)
		kunden = frappe.db.sql("""SELECT `name` FROM `tabCustomer` WHERE YEAR(`creation`) = '{year}'{customer_filter}""".format(year=filters.year, customer_filter=customer_filter), as_dict=True)
		for kunde in kunden:
			alle_faelle = """(SELECT `name` FROM `tabTouche Fall` WHERE `kunde` = '{kunde}')""".format(kunde=kunde.name)
			# alle beratungen
			beratungen = frappe.db.sql("""SELECT `name` FROM `tabTouche Beratung` WHERE `fall` IN {alle_faelle} AND YEAR(`datum`) = '{year}'""".format(alle_faelle=alle_faelle, year=filters.year), as_list=True)
			if len(beratungen) > 0:
				anz += 1
			# beratungen "Betroffene"
			beratungen = frappe.db.sql("""SELECT COUNT(`name`) FROM `tabTouche Beratung` WHERE `fall` IN {alle_faelle} AND YEAR(`datum`) = '{year}' AND `beratung_an` = 'Betroffener'""".format(alle_faelle=alle_faelle, year=filters.year), as_list=True)
			anz_betroffene += beratungen[0][0]
			# beratungen "Angehörige"
			beratungen = frappe.db.sql("""SELECT COUNT(`name`) FROM `tabTouche Beratung` WHERE `fall` IN {alle_faelle} AND YEAR(`datum`) = '{year}' AND `beratung_an` = 'Angehöriger / Bezugsperson'""".format(alle_faelle=alle_faelle, year=filters.year), as_list=True)
			anz_angehoerige += beratungen[0][0]
		_data = []
		_data.append("Im Jahr {year} wurden total {kunden} neu angelegt.".format(year=filters.year, kunden=len(kunden)))
		data.append(_data)
		_data = []
		_data.append("Davon wurden im Jahr {year} insgesamt {anz} mindestens einmal beraten.".format(year=filters.year, anz=anz))
		data.append(_data)
		_data = []
		_data.append('Diese {anz} Kunden wurden wie folgt Beraten; "Betroffene": {anz_betroffene}, "Angehörige / Bezugsperson": {anz_angehoerige}'.format(anz=anz, anz_betroffene=anz_betroffene, anz_angehoerige=anz_angehoerige))
		data.append(_data)
	return columns, data
	
def get_alle_kunden(filters):
	customer_filter = ''
	if filters.iv_leistungen:
		customer_filter = """ WHERE `iv_status` = '{iv_leistungen}'""".format(iv_leistungen=filters.iv_leistungen)
	customers = frappe.db.sql("""SELECT `name`, `iv_status` FROM `tabCustomer`{customer_filter}""".format(customer_filter=customer_filter), as_dict=True)
	return customers
	
def get_alle_kunden_nach_kanton(filters, kanton):
	customer_filter = ''
	if filters.iv_leistungen:
		customer_filter = """ AND `iv_status` = '{iv_leistungen}'""".format(iv_leistungen=filters.iv_leistungen)
	customers = frappe.db.sql("""SELECT `name`, `iv_status` FROM `tabCustomer` WHERE `kanton` = '{kanton}'{customer_filter}""".format(kanton=kanton, customer_filter=customer_filter), as_dict=True)
	return customers

def get_alle_faelle_pro_kunde(kunde):
	faelle = frappe.db.sql("""SELECT `name` FROM `tabTouche Fall` WHERE `kunde` = '{customer}'""".format(customer=kunde), as_list=True)
	return faelle
	
def get_alle_beratungen_zu_faelle(faelle, filters):
	#frappe.throw(str(faelle))
	faelle = str(faelle).replace("[[", "").replace("]]", "").replace("], [", ", ")
	if not filters.beratungstyp:
		beratungstyp_filter = ''
	else:
		beratungstyp_filter = """ AND `beratung_an` = '{beratungstyp}'""".format(beratungstyp=filters.beratungstyp)
	try:
		beratungen = frappe.db.sql("""SELECT `name`
										FROM `tabTouche Beratung`
										WHERE `fall` IN ({alle_faelle})
										AND YEAR(`datum`) = '{year}'
										{beratungstyp_filter}""".format(alle_faelle=faelle, year=filters.year, beratungstyp_filter=beratungstyp_filter), as_list=True)
	except:
		frappe.throw("""SELECT `name`
		FROM `tabTouche Beratung`
		WHERE `fall` IN ({alle_faelle})
		AND YEAR(`datum`) = '{year}'
		{beratungstyp_filter})""".format(alle_faelle=faelle, year=filters.year, beratungstyp_filter=beratungstyp_filter))
	return beratungen
	
def get_summe_in_min_basierend_auf_beratungen(beratungen):
	beratungen = str(beratungen).replace("[[", "").replace("]]", "").replace("], [", ", ")
	minuten = frappe.db.sql("""SELECT SUM(`dauer_in_min`) FROM `tabBeratungs Timesheet` WHERE `parent` IN ({beratungen})""".format(beratungen=beratungen), as_list=True)
	if minuten[0][0]:
		return minuten[0][0]
	else:
		return 0
	
def get_anzahl_beratungen_pro_fall(filters, fall):
	if not filters.beratungstyp:
		beratungstyp_filter = ''
	else:
		beratungstyp_filter = """ AND `beratung_an` = '{beratungstyp}'""".format(beratungstyp=filters.beratungstyp)
	anz_beratungen = frappe.db.sql("""SELECT COUNT(`name`)
										FROM `tabTouche Beratung`
										WHERE `fall` = '{fall}'
										AND YEAR(`datum`) = '{year}'
										{beratungstyp_filter}""".format(fall=fall, year=filters.year, beratungstyp_filter=beratungstyp_filter), as_list=True)
	if anz_beratungen[0][0]:
		if anz_beratungen[0][0] > 0:
			return anz_beratungen[0][0]
		else:
			return 0
	else:
		return 0