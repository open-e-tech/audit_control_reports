# Copyright (c) 2013, hello@openetech.com and contributors
# For license information, please see license.txt
import frappe
from frappe import _
from frappe.utils import flt,cstr
import json
import re

def execute(filters=None):
	columns, data, chart = [], [], []
	columns = get_columns()
	data = get_audit_trail_data(filters)
	return columns, data, None

def get_columns():

	columns = [
		{ 
			"label": _("Document Type"), 
			"fieldtype": "Link", 
			"options": "DocType", 
			"fieldname": "ref_doctype", 
			"width": 200
		},
		{ 
			"label": "Document Reference", 
			"fieldtype": "Dynamic Link", 
			"options": "ref_doctype", 
			"fieldname": "docname", 
			"width": 200
		},
		{
			"fieldname": "modified_by",
			"label": _("Last Updated by"),
			"fieldtype": "Data",
			"width": 200
		},
		{
			"fieldname": "modified",
			"label": _("Last Updated Time"),
			"fieldtype": "Datetime",
			"width": 200
		},
		{
			"fieldname": "submitted",
			"label": _("Submitted"),
			"fieldtype": "Data",
			"width": 100
		},		
		{
			"fieldname": "audit_trail_detail",
			"label": _("System Audit Log"),
			"fieldtype": "Long Text",
			"width": 500
		},
	]

	return columns

def get_conditions(filters):
	conditions = ""
	if filters.get("ref_doctype"):
		conditions += " ref_doctype=%(ref_doctype)s"
	if filters.get('from_date') and filters.get('to_date'):
		conditions += " and DATE(modified)>=%(from_date)s and DATE(modified)<=%(to_date)s"
 
	return conditions
	
def get_audit_trail_data(filters):
	conditions = get_conditions(filters)
	print("conditions")
	print(conditions)
	data = frappe.db.sql('''select ref_doctype,
								docname,
								data as "audit_trail_detail",
								owner,
								modified_by,
								modified
							from 
								`tabVersion`
							where
								{conditions}
							order by
								docname
						'''.format(conditions=conditions),filters,as_dict=1)
	dl=list(data)
	dict_submit = {}
	for row in dl:
		temp_json = json.loads(row['audit_trail_detail'])
		temp_str = json.dumps(temp_json,ensure_ascii=True,skipkeys=True,indent = 6,separators =(". ", " = "))
		row['submitted'] = "No"
		if "changed" in temp_json:
			for d in temp_json['changed']:
				if d[0] == 'docstatus':
					if d[1] == 0 and d[2] == 1:
						row['submitted'] = "Yes"
						dict_submit.setdefault(row['docname'], frappe._dict()).setdefault("modified", []).append(row["modified"])
					else:
						row['submitted'] = "No"
		row['audit_trail_detail'] = temp_str

	for row in dl:
		modified = ''
		if row['docname'] in dict_submit:
			modified = dict_submit.get(row['docname'], {}).get("modified", [])[0]
		if modified:
			if (row['modified'] - modified).days > 0 and row['submitted'] == 'No':
				row['submitted'] = "After Submit"
			elif (row['modified'] - modified).days == 0 and row['submitted'] == 'No' and (row['modified'] - modified).seconds > 0:
				row['submitted'] = "After Submit"
	return dl

