# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class MailingDomain(models.Model):
	_name = 'mailing.domain'
	_description = 'Mailing domains'

	name = fields.Char('Name')
	mailing_domain = fields.Char('Domain', default="[]")
	active = fields.Boolean('Active', default=True)


class MailingMailing(models.Model):
	_inherit = 'mailing.mailing'

	mailing_domain_id = fields.Many2one('mailing.domain', 'Domain')

	@api.onchange('mailing_domain_id')
	def onchange_mailing_domain(self):
		self.mailing_domain = self.mailing_domain_id.mailing_domain


	def call_save_domain(self):
		return {
		        'name':_("Save Mail Domain"),
		        'view_mode': 'form',
		        #'view_id': view_id
		        'view_type': 'form',
		        'res_model': 'mailing.domain.wizard',
		        'type': 'ir.actions.act_window',
		        'target': 'new',
		        'context': {'default_mailing_domain':self.mailing_domain}
		    }
