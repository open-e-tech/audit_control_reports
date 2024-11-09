# Copyright (c) 2024, hello@openetech.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _


class MakerCheckerSettings(Document):
	pass

def validate_maker_checker(self, method):
	mk_chk_settings = frappe.get_doc("Maker Checker Settings")
	if frappe.session.user == self.owner and \
			((self.doctype == "Journal Entry" and mk_chk_settings.journal_entry) or \
  			(self.doctype == "Sales Invoice" and mk_chk_settings.sales_invoice) or \
			(self.doctype == "Purchase Invoice" and mk_chk_settings.purchase_invoice) or \
			(self.doctype == "Payment Entry" and mk_chk_settings.payment_entry) ):
		frappe.throw(_("Creator of the document cannot Submit the document."))