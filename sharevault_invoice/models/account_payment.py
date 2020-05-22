# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.tools.misc import formatLang, format_date

INV_LINES_PER_STUB = 9

class AccountPayment(models.Model):

	_inherit = 'account.payment'

	def _check_build_page_info(self, i, p):
		multi_stub = self.company_id.account_check_printing_multi_stub
		invoice_vals = self._check_make_stub_line2()
		return {
			'sequence_number': self.check_number if (self.journal_id.check_manual_sequencing and self.check_number != 0) else False,
			'payment_date': format_date(self.env, self.payment_date),
			'partner_id': self.partner_id,
			'partner_name': self.partner_id.name,
			'currency': self.currency_id,
			'state': self.state,
			'amount': formatLang(self.env, self.amount, currency_obj=self.currency_id) if i == 0 else 'VOID',
			'amount_in_word': self._check_fill_line(self.check_amount_in_words) if i == 0 else 'VOID',
			'memo': self.communication,
			'stub_cropped': not multi_stub and len(self.invoice_ids) > INV_LINES_PER_STUB,
			# If the payment does not reference an invoice, there is no stub line to display
			'stub_lines': p,
			'stub_lines2': invoice_vals if invoice_vals else []
		}

	def _check_make_stub_line(self, invoice):
		""" Return the dict used to display an invoice/refund in the stub
		"""
		# Find the account.partial.reconcile which are common to the invoice and the payment
		if invoice.type in ['in_invoice', 'out_refund']:
			invoice_sign = 1
			invoice_payment_reconcile = invoice.line_ids.mapped('matched_debit_ids').filtered(lambda r: r.debit_move_id in self.move_line_ids)
		else:
			invoice_sign = -1
			invoice_payment_reconcile = invoice.line_ids.mapped('matched_credit_ids').filtered(lambda r: r.credit_move_id in self.move_line_ids)

		if self.currency_id != self.journal_id.company_id.currency_id:
			amount_paid = abs(sum(invoice_payment_reconcile.mapped('amount_currency')))
		else:
			amount_paid = abs(sum(invoice_payment_reconcile.mapped('amount')))

		amount_residual = invoice_sign * invoice.amount_residual
		invoice_type = self.get_invoice_type(invoice)
		# invoice_lines = self._check_make_stub_line2(invoice)
		return {
			'due_date': format_date(self.env, invoice.invoice_date_due),
			'invoice_date' : format_date(self.env, invoice.invoice_date),
			'invoice_type' : invoice_type,
			'number': invoice.ref and invoice.name + '-' + invoice.ref or invoice.name,
			'amount_total': formatLang(self.env, invoice_sign * invoice.amount_total, currency_obj=invoice.currency_id),
			'amount_residual': formatLang(self.env, amount_residual, currency_obj=invoice.currency_id) if amount_residual * 10**4 != 0 else '-',
			'amount_paid': formatLang(self.env, invoice_sign * amount_paid, currency_obj=invoice.currency_id),
			'currency': invoice.currency_id,
		}

	def _check_make_stub_line2(self):
		""" Return the dict used to display an invoice/refund in the stub
		"""
		vals = []
		for invoice in self.reconciled_invoice_ids:
			if invoice.invoice_line_ids:
				for line in invoice.invoice_line_ids:
					if line.credit == 0.0:
						invoice_lines = {
							'invoice_date' : format_date(self.env, line.move_id.invoice_date),
							'account_number' : line.account_id.code + ' ' + line.account_id.name,
							'analytic_account': line.analytic_account_id.name,
							'description': line.name or line.product_id.name,
							'amount_total': formatLang(self.env, line.price_total, currency_obj=line.move_id.currency_id),
						}
						vals.append(invoice_lines)
		return vals

	def get_invoice_type(self,invoice):
		""" Return invoice type to stub"""
		if invoice.type == 'entry':
			return 'Journal Entry'
		elif invoice.type == 'out_invoice':
			return 'Customer Invoice'
		elif invoice.type == 'out_refund':
			return 'Customer Credit Note'
		elif invoice.type == 'in_invoice':
			return 'Vendor Bill'
		elif invoice.type == 'in_refund':
			return 'Vendor Credit Note'
		elif invoice.type == 'out_receipt':
			return 'Sales Receipt'
		elif invoice.type == 'in_receipt':
			return 'Purchase Receipt'