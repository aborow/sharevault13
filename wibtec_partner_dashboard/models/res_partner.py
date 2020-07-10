# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class Partner(models.Model):
    _inherit = "res.partner"

    def get_partner_dashboard(self):
        for item in self:
            return {
                    'name': _('Dashboard'),
                    'view_mode': 'form',
                    'res_model': 'board.board',
                    'binding_model': 'res.partner',
                    'view_id': self.env.ref('wibtec_partner_dashboard.board_partner_form').id,
                    'type': 'ir.actions.act_window',
                    'context': {
                                'default_partner_id': item.id,
                    },
            }
