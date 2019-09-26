# -*- coding: utf-8 -*-
# Copyright (c) 2013, libracore and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	columns, data = ["Konto::200", "Betrag Vereinnahmt:Currency:200", "Betrag GuV:Currency:200", "Erreichung::100"], []
	
	sql_query = """SELECT 
		   `data`.`account` AS `Konto`,
		   SUM(`data`.`amount`) AS `Betrag`,
		   (SELECT SUM(`tabGL Entry`.`credit` - `tabGL Entry`.`debit`) FROM `tabGL Entry` WHERE `tabGL Entry`.`account` = `data`.`account` AND `tabGL Entry`.`posting_date` >= CONCAT(YEAR(CURDATE()), "-01-01")
			AND `tabGL Entry`.`posting_date` <= CONCAT(YEAR(CURDATE()), "-12-31")) AS `Betrag_GL`
		FROM
		(SELECT 
		  `tabSales Invoice Item`.`income_account` AS `account`,
		  SUM(`tabSales Invoice Item`.`amount`) AS `amount`
		FROM `tabSales Invoice Item`
		LEFT JOIN `tabSales Invoice` ON `tabSales Invoice`.`name` = `tabSales Invoice Item`.`parent` 
		WHERE 
		  `tabSales Invoice`.`docstatus` = 1
		  AND `tabSales Invoice`.`posting_date` >= CONCAT(YEAR(CURDATE()), "-01-01")
		  AND `tabSales Invoice`.`posting_date` <= CONCAT(YEAR(CURDATE()), "-12-31")
		  AND `tabSales Invoice`.`status` = "Paid"
		GROUP BY `tabSales Invoice Item`.`income_account`
		UNION SELECT
		  `tabJournal Entry Account`.`account` AS `account`,
		  SUM(`tabJournal Entry Account`.`credit` - `tabJournal Entry Account`.`debit`) AS `amount`
		FROM `tabJournal Entry Account` 
		LEFT JOIN `tabJournal Entry` ON `tabJournal Entry`.`name` = `tabJournal Entry Account`.`parent`
		WHERE `tabJournal Entry Account`. `account_type` IN ('Income Account', 'Expense Account')
		  AND `tabJournal Entry`.`docstatus` = 1
		  AND `tabJournal Entry`.`posting_date` >= CONCAT(YEAR(CURDATE()), "-01-01")
		  AND `tabJournal Entry`.`posting_date` <= CONCAT(YEAR(CURDATE()), "-12-31")
		GROUP BY `tabJournal Entry Account`.`account`) AS `data`
		GROUP BY `data`.`account`
		ORDER BY `data`.`account` ASC"""
		
	__data = frappe.db.sql(sql_query, as_dict=True)
	ertrag_summe = 0
	gl_ertrag_summe = 0
	_ertrag = []
	aufwand_summe = 0
	gl_aufwand_summe = 0
	_aufwand = []
	for _data in __data:
		if _data["Betrag"] >= 0:
			ertrag_summe += float(_data["Betrag"])
			gl_ertrag_summe += float(_data["Betrag_GL"])
			_ertrag.append([_data["Konto"], _data["Betrag"], _data["Betrag_GL"]])
		else:
			aufwand_summe += float(_data["Betrag"])
			gl_aufwand_summe += float(_data["Betrag_GL"])
			_aufwand.append([_data["Konto"], _data["Betrag"], _data["Betrag_GL"]])
			
	data.append(["3 - Erträge", "", "", ""])
	
	for ertrag in _ertrag:
		data.append([ertrag[0], ertrag[1], ertrag[2], "{0:.2f}".format(((100/ertrag[2]) * ertrag[1])) + "%"])
		
	data.append(["Total", ertrag_summe, gl_ertrag_summe, "{0:.2f}".format(((100/gl_ertrag_summe) * ertrag_summe)) + "%"])
	data.append(["", "", "", ""])
	
	data.append(["4 - Aufwände", "", "", ""])
	for aufwand in _aufwand:
		data.append([aufwand[0], aufwand[1], aufwand[2], "{0:.2f}".format(((100/aufwand[2]) * aufwand[1])) + "%"])
		
	data.append(["Total", aufwand_summe, gl_aufwand_summe, "{0:.2f}".format(((100/gl_aufwand_summe) * aufwand_summe)) + "%"])
	data.append(["", "", "", ""])
	data.append(["Gewinn / Verlust", ertrag_summe + aufwand_summe, gl_ertrag_summe + gl_aufwand_summe, "{0:.2f}".format(((100/(gl_ertrag_summe + gl_aufwand_summe)) * (ertrag_summe + aufwand_summe))) + "%"])
	
	return columns, data
