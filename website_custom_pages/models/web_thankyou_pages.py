# -*- coding: utf-8 -*-
from odoo import models, fields,api, _


class WebThankYouPages(models.Model):
    _name = "web.thankyou.pages"
    _description = "Thank you Pages on sharevault website form"

    name = fields.Char('Name')
    text = fields.Html('Text')
    active = fields.Boolean('Active')


class ResCompany(models.Model):

    _inherit = "res.company"

    typ_id = fields.Many2one('web.thankyou.pages', 'Thank You Pages')