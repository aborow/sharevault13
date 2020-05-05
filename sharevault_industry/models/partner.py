# -*- coding: utf-8 -*-
import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class Partner(models.Model):
    _inherit = 'res.partner'

    industry_tag_ids = fields.Many2many(
                                    'res.partner.industry_tag',
                                    'res_partner_industry_tag_rel',
                                    'partner_id', 'industry_tag_id',
                                    string="Industry (TAGS)",
                                    )

    @api.onchange('industry_id','subindustry_id')
    @api.depends('industry_id','subindustry_id')
    def get_accindustry(self):
        id = False
        if self.industry_id:
            id = self.industry_id.accindustry_id\
                    and self.industry_id.accindustry_id.id or False
        self.accindustry_id = id


class Subindustry(models.Model):
    _inherit = 'res.partner.subindustry'

    accindustry_id = fields.Many2one('res.partner.industry', 'Accounting Industry')


class Industry(models.Model):
    _inherit = 'res.partner.industry'

    accindustry_id = fields.Many2one('res.partner.industry', 'Accounting Industry')


class IndustryTag(models.Model):
    _name = 'res.partner.industry_tag'
    _description = "Industry tags"
    _order = 'display_name ASC'

    name = fields.Char('Name')
    color = fields.Integer('Color Index')
    parent_id = fields.Many2one('res.partner.industry_tag', 'Parent')
    active = fields.Boolean('Active', default=True)

    def name_get(self):
        if self._context.get('partner_industry_tag_display') == 'short':
            return super(IndustryTag, self).name_get()
        res = []
        for s in self:
            names = []
            current = s
            while current:
                names.append(current.name or "")
                current = current.parent_id
            res.append((s.id, ' / '.join(reversed(names))))
        return res
