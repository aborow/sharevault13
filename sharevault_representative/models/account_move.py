# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class AccountMove(models.Model):
    _inherit = "account.move"

    rep_id = fields.Many2one('sharevault.rep', 'Representative')