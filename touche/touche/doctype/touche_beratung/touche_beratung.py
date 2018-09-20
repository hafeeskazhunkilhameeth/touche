# -*- coding: utf-8 -*-
# Copyright (c) 2018, libracore and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class ToucheBeratung(Document):
	def before_save(self):
		getSummeAufwand(self)


def getSummeAufwand(self):
	#set total time for Beratung
	time = 0
	hh = 0
	mm = 0
	
	for entry in self.get("beratungs_timesheet"):
		time = time + int(entry.dauer_in_min)
		
	if time > 60:
		while time >= 60:
			hh = hh + 1
			time = time - 60
		if time < 10:
			time = "0" + str(time)
		mm = time
	else:
		if time == 60:
			hh = 1
			time = "00"
		else:
			hh = 0
		if time < 10:
			time = "0" + str(time)
		mm = time
		
	self.summe_aufwand = str(hh) + ":" + str(mm)