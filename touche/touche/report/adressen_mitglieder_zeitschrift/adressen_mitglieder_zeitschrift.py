# Copyright (c) 2013, libracore and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	columns, data = [], []
	
	data = frappe.db.sql("""SELECT
								`customer`.`salutation`,
								`contact`.`first_name`,
								`contact`.`last_name`,
								`address`.`address_line1`,
								`address`.`address_line2`,
								`address`.`address_line3`,
								`address`.`pincode`,
								`address`.`city`
							FROM ((((`tabCustomer` AS `customer`
							INNER JOIN `tabDynamic Link` AS `adress_link` ON `customer`.`name` = `adress_link`.`link_name`)
							INNER JOIN `tabAddress` AS `address` ON `adress_link`.`parent` = `address`.`name`)
							INNER JOIN `tabDynamic Link` AS `contact_link` ON `customer`.`name` = `contact_link`.`link_name`)
							INNER JOIN `tabContact` AS `contact` ON `contact_link`.`parent` = `contact`.`name`)
							WHERE
								`address`.`mitglieder_zeitschrift` = 1""", as_list=True)
								
	columns = ["Anrede:Data", "Vorname:Data", "Nachname:Data", "Zeile 1:Data", "Zeile 2:Data", "Zeile 3:Data", "PLZ:Data", "ORT:Data"]
	return columns, data
