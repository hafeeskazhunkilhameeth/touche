# -*- coding: utf-8 -*-
# Copyright (c) 2018, libracore and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class ToucheFall(Document):
	def onload(self):
		hh = 0
		mm = 0
		query = """SELECT `summe_aufwand` FROM `tabTouche Beratung` WHERE `fall` = '{0}'""".format(self.name)
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
			
		self.summe_zeitaufwand = str(hh) + ":" + str(mm)
