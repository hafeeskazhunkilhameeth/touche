# Copyright (c) 2013, libracore and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def update_time():
	falls = frappe.db.sql("""SELECT `name` FROM `tabTouche Fall`""", as_dict=True)
	for fall in falls:
		hh = 0
		mm = 0
		query = """SELECT `summe_aufwand` FROM `tabTouche Beratung` WHERE `fall` = '{fall}'""".format(fall=fall.name)
		times = frappe.db.sql(query, as_list = True)
		for time in times:
			splittet_time = time[0].split(":")
			hh = hh + int(splittet_time[0])
			mm = mm + int(splittet_time[1])
			
		if mm >= 60:
			while mm >= 60:
				hh = hh + 1
				mm = mm - 60
		if mm < 10:
			mm = "0" + str(mm)
			
		frappe.db.sql("""UPDATE `tabTouche Fall` SET `summe_zeitaufwand` = '{neuer_wert}' WHERE `name` = '{fall}'""".format(neuer_wert=str(hh) + ":" + str(mm), fall=fall.name), as_list=True)