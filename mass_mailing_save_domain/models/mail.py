# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

"""
There should be a new feature to enable us to save the filters that we create when we are
	sending a mail to a contact list (not mailing list!).

Next to the code editor, there should be a button. On pop up, we should enter a name and
	the code in the editor plus the name would be a new mail.contact.filter record.

There should be a way to list/edit/delete filters.

In the mail form, there should be a dopdown allowing us to choose a filter. On choosing one,
	the code editor should populate
"""

class MailingDomain(models.Model):
	_name = 'mailing.domain'
	_description = 'Mailing domains'

	name = fields.Char('Name')
	mailing_domain = fields.Char('Domain')
	active = fields.Boolean('Active', default=True)


class MailingDomainWizard(models.TransientModel):
	_name = 'mailing.domain.wizard'
	_description = "Wizard for saving a mailing domain"

	name = fields.Char('Name')
	mailing_domain = fields.Char('Domain')


class MailingMailing(models.Model):
	_inherit = 'mailing.mailing'

	mailing_domain_id = fields.Many2one('mailing.domain', 'Domain')

	@api.onchange('mailing_domain_id')
	def onchange_mailing_domain(self):
		self.mailing_domain = self.mailing_domain_id.mailing_domain
