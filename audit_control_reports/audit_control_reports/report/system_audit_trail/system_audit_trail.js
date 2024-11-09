// Copyright (c) 2024, hello@openetech.com and contributors
// For license information, please see license.txt

frappe.query_reports["System Audit Trail"] = {
	"filters": [
			{
					"fieldname": "ref_doctype",
					"label": __("Document"),
					"fieldtype": "Link",
					"options": "DocType",
					"required": "1",
					"default": "Sales Invoice"
			},
			{
					"fieldname": "from_date",
					"label":__("From Date"),
					"fieldtype": "Date",
					"required": "1",
					"default": frappe.datetime.add_months(frappe.datetime.get_today(), -1)
			},
			{
					"fieldname": "to_date",
					"label":__("To Date"),
					"fieldtype": "Date",
					"required": "1",
					"default": frappe.datetime.add_months(frappe.datetime.get_today())
			}
	]
};
