# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class SharevaultRep(models.Model):
    _name = 'sharevault.rep'
    _description = 'ShareVaults Representative'

    name = fields.Char('Name')
    active = fields.Boolean(default=True)
    abbr = fields.Char(string='Abbreviated', translate=True)