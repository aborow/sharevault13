# -*- coding: utf-8 -*-
import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class Partner(models.Model):
    _inherit = 'res.partner'

    subindustry_ids = fields.Many2many(
                                    'res.partner.subindustry',
                                    'res_partner_subindustry_rel',
                                    'partner_id', 'subindustry_id',
                                    string="Sub Industry",
                                    )


class Subindustry(models.Model):
    _inherit = 'res.partner.subindustry'

    #display name should be calculated (like product category)
    #display_name = fields.Char('Name')
    color = fields.Integer('Color Index')
    parent_id = fields.Many2one('res.partner.subindustry', 'Industry')


    def name_get(self):
        if self._context.get('partner_subindustry_display') == 'short':
            return super(Subindustry, self).name_get()
        res = []
        for s in self:
            names = []
            current = s
            while current:
                names.append(current.name)
                current = current.parent_id
            res.append((s.id, ' / '.join(reversed(names))))
        return res
