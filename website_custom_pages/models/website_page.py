# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError

class WebPage(models.Model):
    _inherit = 'website.page'

    is_template = fields.Boolean('Is a template?')
