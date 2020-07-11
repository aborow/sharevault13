# -*- coding: utf-8 -*-
#import logging
from odoo import api, fields, models, _
#_logger = logging.getLogger(__name__)

class Partner(models.Model):
    _inherit = "res.partner"

    def get_partner_dashboard(self):
        for item in self:
            view = self.env.ref('wibtec_partner_dashboard.board_partner_form')
            return {
                    'type': 'ir.actions.act_window',
                    'name': _('Dashboard'),
                    'view_mode': 'form',
                    'res_model': 'board.board',
                    'binding_model': 'res.partner',
                    'view_id': view.id,
                    'context': {'default_partner_id': item.id}
                    }
