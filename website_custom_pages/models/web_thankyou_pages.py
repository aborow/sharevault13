# -*- coding: utf-8 -*-
from odoo import models, fields,api, _


class WebThankYouPages(models.Model):
    _name = "web.thankyou.pages"
    _description = "Thank you Pages on sharevault website form"

    name = fields.Char('Name')
    text = fields.Html('Text')
    mail_template_id = fields.Many2one('mail.template','Confirmation Email')
    active = fields.Boolean('Active', default=True)

    shared_link_id = fields.Many2one('documents.share', 'Shared Link')


    @api.onchange('shared_link_id')
    def onchange_shared_link_id(self):
        slink = self.shared_link_id
        if slink:
            self.text = self.text.replace('PLACEHOLDER_WHITEPAPER',
                    slink.tracked_link_id \
                    and slink.tracked_link_id.short_url \
                    or slink.full_url)
            # Let's make sure we don't get duplicate http
            self.text = self.text.replace('http://http://','http://')
            self.text = self.text.replace('https://https://','https://')


class MailSuppressionList(models.Model):
    _inherit = 'mail.suppression_list'

    @api.model
    def check_email_domain(self,email):
        result = ''
        if '@' in email:
            domain = email.split('@')[1]
            if domain:
                msl = self.search([('name', '=', domain), ('use_in_webform', '=', True)])
                if msl:
                    result = 'Please Enter new mail'
        return result