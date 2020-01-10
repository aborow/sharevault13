# -*- coding: utf-8 -*-
from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    rep_id = fields.Many2one('sharevault.rep', 'Representative')

    def _prepare_invoice(self):
        result = super(SaleOrder, self)._prepare_invoice()
        if self.rep_id:
            result.update({'rep_id': self.rep_id.id})
        return result
