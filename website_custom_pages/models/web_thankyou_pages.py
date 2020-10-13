# -*- coding: utf-8 -*-
from odoo import models, fields,api, _


class WebThankYouPages(models.Model):
    _name = "web.thankyou.pages"
    _description = "Thank you Pages on sharevault website form"

    name = fields.Char('Name')
    text = fields.Html('Text')
    mail_template_id = fields.Many2one('mail.template','Confirmation Email')
    active = fields.Boolean('Active', default=True)
