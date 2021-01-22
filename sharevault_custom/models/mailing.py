# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _

class MailingTrace(models.Model):
    _inherit = 'mailing.trace'

    @api.depends('model','res_id')
    def _get_partner(self):
        for s in self:
            if s.model=='res.partner' and s.res_id:
                s.partner_id = s.res_id
            else:
                s.partner_id = False

    partner_id = fields.Many2one('res.partner', 'Partner',
                                    compute='_get_partner', store=True)
