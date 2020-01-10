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


class ImportJE(models.TransientModel):
	_name = "import.je"
	_description = "Import Journal Entries"

	file = fields.Binary('Select File')

	def find_account_id(self, account_code):
		if account_code:
			account_ids = self.env['account.account'].search([('code', '=', account_code)])
			if account_ids:
				account_id = account_ids[0]
				return account_id
			else:
				raise Warning(_('"%s" Wrong Account Code') % account_code.split('.'))

	def find_account_analytic_id(self, analytic_account_name):
		analytic_account_id = self.env['account.analytic.account'].search([('name', '=', analytic_account_name)])
		if analytic_account_id:
			analytic_account_id = analytic_account_id[0].id
			return analytic_account_id
		else:
			raise Warning(_('"%s" Wrong Analytic Account Name') % analytic_account_name)

	def create_import_move_lines(self, values):
		move_line_obj = self.env['account.move.line']
		move_obj = self.env['account.move']
		result = {}

		if values.get('Label'):
			label = values.get('Label')
			result.update({'name': label})

		if values.get('Account'):
			account_code = values.get('Account')
			account_id = self.find_account_id(str(account_code))
			if account_id != None:
				result.update({'account_id': account_id.id})
			else:
				raise Warning(_('"%s" Wrong Account Code %s') % account_code)

		if values.get('Debit') != '':
			result.update({'debit': float(values.get('Debit'))})
			if float(values.get('Debit')) < 0:
				result.update({'credit': abs(values.get('Debit'))})
				result.update({'debit': 0.0})
		else:
			result.update({'debit': float('0.0')})

		if values.get('Credit') != '':
			result.update({'credit': float(values.get('Credit'))})
			if float(values.get('Credit')) < 0:
				result.update({'debit': abs(values.get('Credit'))})
				result.update({'credit': 0.0})
		else:
			result.update({'credit': float('0.0')})

		if values.get('Analytic Account') != '':
			account_anlytic_account = values.get('Analytic Account')
			if account_anlytic_account != '' or account_anlytic_account == None:
				analytic_account_id = self.find_account_analytic_id(account_anlytic_account)
				result.update({'analytic_account_id': analytic_account_id})
			else:
				raise Warning(_('"%s" Wrong Account Code %s') % account_anlytic_account)

		return result

	def create_import_hist_lines(self, values):
		result = {}
		if values.get('Hist QB Account Type'):
			hqat = values.get('Hist QB Account Type')
			result.update({'hist_qb_acc_type': hqat})
		if values.get('Hist Partner QB Name'):
			hpqn = values.get('Hist Partner QB Name')
			result.update({'hist_pqb_name':hpqn})
		if values.get('Hist Item'):
			hi = values.get('Hist Item')
			result.update({'hist_item': hi})
		if values.get('Hist Qty'):
			hq = values.get('Hist Qty')
			result.update({'hist_qty': hq})
		if values.get('Hist Sales Price'):
			hsp = values.get('Hist Sales Price')
			result.update({'hist_sales_price': hsp})

		return result

	def import_je(self):
		keys = ['Reference', 'Hist Type', 'Accounting Date', 'Hist Number', 'Hist Partner QB Name',
			'Hist ShareVault Name', 'Label', 'Hist Item', 'Account', 'Analytic Account', 'Hist Representative',
			'Hist Pay Method', 'Hist Qty', 'Hist Sales Price', 'Debit', 'Credit', 'Hist QB Account Type', 'journal']
		csv_data = base64.b64decode(self.file)
		data_file = io.StringIO(csv_data.decode("utf-8"))
		data_file.seek(0)
		file_reader = []
		csv_reader = csv.reader(data_file, delimiter=',')

		try:
			file_reader.extend(csv_reader)
		except Exception:
			raise exceptions.Warning(_("Invalid file!"))

		values = {}
		lines = []
		data = []
		for i in range(len(file_reader)):
			field = list(map(str, file_reader[i]))
			values = dict(zip(keys, field))
			if values:
				if i == 0:
					continue
				else:
					data.append(values)

		data1 = {}
		sorted_data = sorted(data, key=lambda x: x['Reference'])
		list1 = []
		for key, group in itertools.groupby(sorted_data, key=lambda x: x['Reference']):
			small_list = []
			for i in group:
				small_list.append(i)
				data1.update({key: small_list})

		for key in data1.keys():
			move_lines = []
			hist_lines = []
			values = data1.get(key)
			for val in values:
				res = self.create_import_move_lines(val)
				hist_res = self.create_import_hist_lines(val)
				move_obj = self.env['account.move']
				if val.get('journal'):
					journal_search = self.env['account.journal'].search([('name', '=', val.get('journal'))])
					if journal_search:
						input_date = val.get('Accounting Date')
						date = datetime.strptime(input_date, "%d/%m/%Y")
						hist_type = val.get('Hist Type')
						hist_num = val.get('Hist Number')
						hist_sv_name = val.get('Hist ShareVault Name')
						hist_rep = val.get('Hist Representative')
						hist_pay_method = val.get('Hist Pay Method')
						move1 = move_obj.search([('ref', '=', val.get('Reference')),
												 ('journal_id', '=', journal_search.name)])
						if move1:
							move = move1
						else:
							move = move_obj.create({'date': date.date() or False,
								'ref': val.get('Reference') or False,
								 'journal_id': journal_search.id,
								 'hist_type': hist_type,
								 'hist_num': hist_num,
								 'hist_sv_name': hist_sv_name,
								 'hist_rep': hist_rep,
								 'hist_pay_method': hist_pay_method,
								 })
					else:
						raise Warning(_('Please Define Journal which are already in system.'))
				move_lines.append((0, 0, res))
				hist_lines.append((0,0, hist_res))
			move.write({'line_ids': move_lines, 'hist_qba_type_ids': hist_lines})