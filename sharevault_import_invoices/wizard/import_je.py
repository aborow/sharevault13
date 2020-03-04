# -*- coding: utf-8 -*-

from odoo import api, fields, models, _,exceptions
from odoo.exceptions import Warning,ValidationError
from datetime import datetime
import itertools
import logging
_logger = logging.getLogger(__name__)
import io
try:
	import csv
except ImportError:
	_logger.debug('Cannot `import csv`.')
try:
	import StringIO
except ImportError:
	_logger.debug('Cannot `import StringIO`.')
try:
	import base64
except ImportError:
	_logger.debug('Cannot `import base64`.')


class ImportIV(models.TransientModel):
	_name = "import.iv"
	_description = "Import Invoices"

	file = fields.Binary('Select File')
	journal_id = fields.Many2one('account.journal', string='Journal', required=True)

	def find_account_id(self, account_code):
		if account_code:
			account_ids = self.env['account.account'].search([('code', '=', account_code)])
			if account_ids:
				account_id = account_ids[0]
				return account_id
			else:
				raise Warning(_('"%s" Wrong Account Code') % account_code.split('.'))

	def find_partner(self,name):
		partner_id = self.env['res.partner'].search([('name','=',name)],limit=1)
		if partner_id:
			return partner_id
		else:
			raise Warning(_('Partner "%s" is not Available in System.') % name)

	def create_import_move_lines(self, values):
		result = {}
		if values.get('Label'):
			label = values.get('Label')
			result.update({'name': label})
		if values.get('quantity'):
			qty = values.get('quantity')
			result.update({'quantity': float(qty)})
		if values.get('price_unit'):
			price_unit = values.get('price_unit')
			result.update({'price_unit': float(price_unit)})
		return result

	def import_iv(self):
		# Method is used to fetch all data from selected csv file
		if not self.file:
			raise Warning(_('Please Select CSV File.'))
		else:
			keys = ['ref','invoice_date_due', 'invoice_date', 'partner_id', 'hist_num', 'product_id',
					'Label', 'account_id', 'quantity', 'price_unit',]
			try:
				data = base64.b64decode(self.file)
				file_input = io.StringIO(data.decode("utf-8"))
				file_input.seek(0)
				reader = csv.reader(file_input, delimiter=',')
			except ValueError:
				raise ValidationError(_('Not a Valid File!'))
			reader_info = []
			reader_info.extend(reader)
			values = {}
			for i in range(len(reader_info)):
				field = map(str, reader_info[i])
				values = dict(zip(keys, field))
				if values:
					if values['ref'] == 'ref':
						continue
					res = self.create_inv(values)
			return res

	def create_inv(self,values):
		res = self.create_import_move_lines(values)
		move_obj = self.env['account.move']
		input_date = values.get('invoice_date')
		date = datetime.strptime(input_date, "%m/%d/%Y")
		due_date = values.get('invoice_date_due')
		dd = False
		if due_date:
			dd = datetime.strptime(due_date, "%m/%d/%Y").date()
		invoice_date_due = dd
		invoice_date = date
		hist_num = values.get('Hist Number')
		partner_id = self.find_partner(values.get('partner_id'))
		if res:
			context = dict(self._context or {})
			context.update({
				'journal_id': self.journal_id.id,
				'default_type': 'out_invoice'
			})
			move_obj = self.env["account.move"].with_context(context)
			move_line_obj = self.env["account.move.line"].with_context(context)
			abc = move_line_obj.default_get(list(move_line_obj._fields))
			move_line = move_line_obj.new(abc)
			move_line_vals = move_line._convert_to_write(
				{name: move_line[name] for name in move_line._cache})
			res['exclude_from_invoice_tab'] = False
			move_line_vals.update(res)
			move_vals = move_obj.new({
				'ref': values.get('ref') or False,
				'hist_num': hist_num,
				'partner_id': partner_id.id or False,
				'invoice_date_due': invoice_date_due or False,
				'invoice_date': invoice_date.date(),
				'type': 'out_invoice',
			})
			main_move_vals = move_vals._convert_to_write(
				{name: move_vals[name] for name in move_vals._cache})
			main_move_vals.update({
				'invoice_line_ids': [(0, 0, move_line_vals)]
			})
			move_vals._onchange_invoice_line_ids()
			ml = move_obj.create(main_move_vals)
			if ml:
				for line in ml.line_ids:
					if line.account_id.user_type_id.type == "receivable":
						account_id = self.find_account_id(values.get('account_id'))
						line.write({'account_id': account_id.id})
