# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import Warning,ValidationError
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


class UpdateCustomers(models.TransientModel):

	_name = "update.customers"
	_description = "Update Customers"

	file = fields.Binary(string="Upload your File")

	def update_customer(self):
		# Method is used to fetch all data from selected csv file
		if not self.file:
			raise Warning(_('Please Select CSV File.'))
		else:
			keys = ['Name','Customer Rank','Supplier Rank']
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
					if values['Name'] == 'Name':
						continue
					res = self.update_partner(values)
			return res

	def update_partner(self,values):
		partner_id = self.find_partner(values.get('Name'))
		if partner_id:
			partner_id.write({'customer_rank': values.get('Customer Rank')})
			partner_id.write({'supplier_rank': values.get('Supplier Rank')})

	def find_partner(self,name):
		partner_id = self.env['res.partner'].search([('name','=',name)],limit=1)
		if partner_id:
			return partner_id
		else:
			raise Warning(_('Partner "%s" is not Available in System.') % name)
