# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class Filter(models.Model):
	_inherit = 'ir.filters'

	mailing_domain_id = fields.Many2one('mailing.domain', 'Saved filter')
