# -*- coding: utf-8 -*-
from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        super(SaleOrder, self).onchange_partner_id()
        if self.partner_id.company_type == 'company':
            return {'domain': {'sharevault_id': [('partner_id', '=', self.partner_id.id)]}}
        if self.partner_id.company_type == 'person':
            return {'domain': {'sharevault_id': [('sharevault_owner', '=', self.partner_id.id)]}}


    sharevault_id = fields.Many2one('sharevault.sharevault', 'ShareVault',
                                        readonly=True,
                                        states={'draft': [('readonly', False)]})
    sales_type = fields.Selection([('new', 'New Customer'),
                                   ('cs', 'Customer Success'),
                                   ('renewal', 'Renewal')], string="Sales Type")

    def _prepare_invoice(self):
        result = super(SaleOrder, self)._prepare_invoice()
        if self.sales_type:
            result.update({'sales_type': self.sales_type})
        if self.sharevault_id:
            result.update({'sharevault_id': self.sharevault_id.id})
        return result
