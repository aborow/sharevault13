# -*- coding: utf-8 -*-
from odoo import api, fields, models, _, SUPERUSER_ID


class ResPartner(models.Model):
    _inherit = "res.partner"

    odoo_score = fields.Float('Odoo Score')