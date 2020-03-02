# Copyright (c) 2013, libracore and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	#columns, data = ["Kunde:Link/Customer", "Fälle:Data", "IV-Leistung:Data", "Summe Zeitaufwand (h:mm):Data"], []
	columns, data = [], []
	if filters.beratungstyp:
		beratungstyp = " AND `name` IN (SELECT `fall` FROM `tabTouche Beratung` WHERE `beratung_an` = '{beratungstyp}')".format(beratungstyp=filters.beratungstyp)
	
	if filters.auswertungstyp == 'Beratungsstunden':
		columns, data = ["Kunde:Link/Customer", "Fälle:Data", "IV-Leistung:Data", "Summe Zeitaufwand (h:mm):Data"], []
		alle_faelle_filter = " WHERE YEAR(`creation`) = '{year}'".format(year=filters.year)
		if filters.iv_leistungen:
			alle_faelle_filter += " AND `iv_leistungen` = '{iv_leistungen}'".format(iv_leistungen=filters.iv_leistungen)
		if filters.customer:
			alle_faelle_filter += " AND `kunde` = '{kunde}'".format(kunde=filters.customer)
		alle_kunden = frappe.db.sql("""SELECT DISTINCT `kunde` FROM `tabTouche Fall`{alle_faelle_filter}{beratungstyp}""".format(alle_faelle_filter=alle_faelle_filter, beratungstyp=beratungstyp), as_dict=True)
		total_std = 0
		total_min = 0
		for kunde in alle_kunden:
			data_to_append = []
			data_to_append.append(kunde.kunde)
			faelle_pro_kunde = ''
			iv_leistungen = ''
			std = 0
			min = 0
			alle_faelle = frappe.db.sql("""SELECT * FROM `tabTouche Fall`{alle_faelle_filter} AND `kunde` = '{kunde}'{beratungstyp}""".format(alle_faelle_filter=alle_faelle_filter, kunde=kunde.kunde, beratungstyp=beratungstyp), as_dict=True)
			if len(alle_faelle) > 0:
				for fall in alle_faelle:
					if fall.summe_zeitaufwand:
						splittet_time = fall.summe_zeitaufwand.split(":")
						std += int(splittet_time[0])
						min += int(splittet_time[1])
						total_std += int(splittet_time[0])
						total_min += int(splittet_time[1])
						
					if faelle_pro_kunde == '':
						faelle_pro_kunde = fall.name
					else:
						faelle_pro_kunde += ', ' + fall.name
					iv_leistungen = fall.iv_leistungen
				
				while min > 60:
					std += 1
					min -= 60
				if min == 60:
					std += 1
					min = 0
				if min < 10:
					min = "0" + str(min)
						
				data_to_append.append(faelle_pro_kunde)
				data_to_append.append(iv_leistungen)
				data_to_append.append(str(std) + ":" + str(min))
				data.append(data_to_append)
			else:
				data_to_append.append(faelle_pro_kunde)
				data_to_append.append(iv_leistungen)
				data_to_append.append("00:00")
				data.append(data_to_append)
			
		while total_min > 60:
			total_std += 1
			total_min -= 60
		if total_min == 60:
			total_std += 1
			total_min = 0
		if total_min < 10:
			total_min = "0" + str(total_min)
		data.append(["Total Kunden:", str(len(alle_kunden)), "Total Zeitaufwand:", str(total_std) + ":" + str(total_min)])
	elif filters.auswertungstyp == 'Neukunden':
		if filters.beratungstyp:
			beratungstyp = " AND `name` IN (SELECT `fall` FROM `tabTouche Beratung` WHERE `beratung_an` = '{beratungstyp}')".format(beratungstyp=filters.beratungstyp)
		alle_kunden = frappe.db.sql("""SELECT DISTINCT `kunde`
										FROM `tabTouche Fall`
										WHERE YEAR(`creation`) = '{year}'
										AND `kunde` IN (SELECT `name` FROM `tabCustomer` WHERE YEAR(`creation`) = '{year}'){beratungstyp}""".format(year=filters.year, beratungstyp=beratungstyp), as_dict=True)
		columns, data = ["Anzahl Neukunden mit Beratung(en) in {year}:Data:300".format(year=filters.year)], []
		if len(alle_kunden) > 0:
			data.append([str(len(alle_kunden))])
		else:
			data.append(["0"])
	elif filters.auswertungstyp == 'nach Kanton':
		typ_filter = ''
		if filters.iv_leistungen:
			typ_filter = " AND `tabFall`.`iv_leistungen` = '{iv_leistungen}'".format(iv_leistungen=filters.iv_leistungen)
		if filters.beratungstyp:
			beratungstyp = " AND `tabFall`.`name` IN (SELECT `fall` FROM `tabTouche Beratung` WHERE `beratung_an` = '{beratungstyp}')".format(beratungstyp=filters.beratungstyp)
		alle_kunden = frappe.db.sql("""SELECT DISTINCT `tabFall`.`kunde`,
										`tabKunde`.`kanton`
										FROM `tabTouche Fall` AS `tabFall`
										INNER JOIN `tabCustomer` AS `tabKunde`
										ON `tabFall`.`kunde` = `tabKunde`.`name`
										WHERE YEAR(`tabFall`.`creation`) = '{year}'{typ_filter}{beratungstyp}""".format(year=filters.year, typ_filter=typ_filter, beratungstyp=beratungstyp), as_dict=True)
		columns, data = ["Kanton:Data", "Anzahl:Int"], []
		verwendete_kantone = {}
		if len(alle_kunden) > 0:
			#data.append([str(len(alle_kunden))])
			for kunde in alle_kunden:
				if kunde.kanton not in verwendete_kantone:
					verwendete_kantone[kunde.kanton] = 1
				else:
					verwendete_kantone[kunde.kanton] += 1
			for key in verwendete_kantone:
				data.append([key, verwendete_kantone[key]])
				#frappe.throw(str(key) + "...." + str(value))
		else:
			data.append(["Alle", "0"])
	else:
		columns, data = [], []
	return columns, data