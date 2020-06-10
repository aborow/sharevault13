# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class MailingDomainWizard(models.TransientModel):
	_name = 'mailing.domain.wizard'
	_description = "Wizard for saving a mailing domain"

	name = fields.Char('Name')
	mailing_domain = fields.Char('Domain', default="[]")

	def create_domain(self):
		self.env['mailing.domain'].create({
											'name': self.name,
											'mailing_domain': self.mailing_domain
											})
